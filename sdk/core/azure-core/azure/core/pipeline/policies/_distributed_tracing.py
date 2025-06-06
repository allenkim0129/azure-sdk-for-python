# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# --------------------------------------------------------------------------
"""Traces network calls using the implementation library from the settings."""
import logging
import sys
import urllib.parse
from typing import TYPE_CHECKING, Optional, Tuple, TypeVar, Union, Any, Type, Mapping, Dict
from types import TracebackType

from azure.core.pipeline import PipelineRequest, PipelineResponse
from azure.core.pipeline.policies import SansIOHTTPPolicy
from azure.core.pipeline.transport import (
    HttpResponse as LegacyHttpResponse,
    HttpRequest as LegacyHttpRequest,
)
from azure.core.rest import HttpResponse, HttpRequest
from azure.core.settings import settings
from azure.core.tracing import SpanKind
from azure.core.tracing.common import change_context
from azure.core.instrumentation import get_tracer
from azure.core.tracing._models import TracingOptions

if TYPE_CHECKING:
    from opentelemetry.trace import Span

HTTPResponseType = TypeVar("HTTPResponseType", HttpResponse, LegacyHttpResponse)
HTTPRequestType = TypeVar("HTTPRequestType", HttpRequest, LegacyHttpRequest)
ExcInfo = Tuple[Type[BaseException], BaseException, TracebackType]
OptExcInfo = Union[ExcInfo, Tuple[None, None, None]]

_LOGGER = logging.getLogger(__name__)


def _default_network_span_namer(http_request: HTTPRequestType) -> str:
    """Extract the path to be used as network span name.

    :param http_request: The HTTP request
    :type http_request: ~azure.core.pipeline.transport.HttpRequest
    :returns: The string to use as network span name
    :rtype: str
    """
    return http_request.method


class DistributedTracingPolicy(SansIOHTTPPolicy[HTTPRequestType, HTTPResponseType]):
    """The policy to create spans for Azure calls.

    :keyword network_span_namer: A callable to customize the span name
    :type network_span_namer: callable[[~azure.core.pipeline.transport.HttpRequest], str]
    :keyword tracing_attributes: Attributes to set on all created spans
    :type tracing_attributes: dict[str, str]
    :keyword instrumentation_config: Configuration for the instrumentation providers
    :type instrumentation_config: dict[str, Any]
    """

    TRACING_CONTEXT = "TRACING_CONTEXT"
    _SUPPRESSION_TOKEN = "SUPPRESSION_TOKEN"

    # Current stable HTTP semantic conventions
    _HTTP_RESEND_COUNT = "http.request.resend_count"
    _USER_AGENT_ORIGINAL = "user_agent.original"
    _HTTP_REQUEST_METHOD = "http.request.method"
    _URL_FULL = "url.full"
    _HTTP_RESPONSE_STATUS_CODE = "http.response.status_code"
    _SERVER_ADDRESS = "server.address"
    _SERVER_PORT = "server.port"
    _ERROR_TYPE = "error.type"

    # Azure attributes
    _REQUEST_ID = "x-ms-client-request-id"
    _REQUEST_ID_ATTR = "az.client_request_id"
    _RESPONSE_ID = "x-ms-request-id"
    _RESPONSE_ID_ATTR = "az.service_request_id"

    def __init__(self, *, instrumentation_config: Optional[Mapping[str, Any]] = None, **kwargs: Any):
        self._network_span_namer = kwargs.get("network_span_namer", _default_network_span_namer)
        self._tracing_attributes = kwargs.get("tracing_attributes", {})
        self._instrumentation_config = instrumentation_config

    def on_request(self, request: PipelineRequest[HTTPRequestType]) -> None:
        """Starts a span for the network call.

        :param request: The PipelineRequest object
        :type request: ~azure.core.pipeline.PipelineRequest
        """
        ctxt = request.context.options
        try:
            tracing_options: TracingOptions = ctxt.pop("tracing_options", {})
            tracing_enabled = settings.tracing_enabled()

            # User can explicitly disable tracing for this request.
            user_enabled = tracing_options.get("enabled")
            if user_enabled is False:
                return

            # If tracing is disabled globally and user didn't explicitly enable it, don't trace.
            if not tracing_enabled and user_enabled is None:
                return

            span_impl_type = settings.tracing_implementation()
            namer = ctxt.pop("network_span_namer", self._network_span_namer)
            tracing_attributes = ctxt.pop("tracing_attributes", self._tracing_attributes)
            span_name = namer(request.http_request)

            span_attributes = {**tracing_attributes, **tracing_options.get("attributes", {})}

            if span_impl_type:
                # If the plugin is enabled, prioritize it over the core tracing.
                span = span_impl_type(name=span_name, kind=SpanKind.CLIENT)
                for attr, value in span_attributes.items():
                    span.add_attribute(attr, value)  # type: ignore

                with change_context(span.span_instance):
                    headers = span.to_header()
                    request.http_request.headers.update(headers)
                request.context[self.TRACING_CONTEXT] = span
            else:
                # Otherwise, use the core tracing.
                config = self._instrumentation_config or {}
                tracer = get_tracer(
                    library_name=config.get("library_name"),
                    library_version=config.get("library_version"),
                    attributes=config.get("attributes"),
                )
                if not tracer:
                    _LOGGER.warning(
                        "Tracing is enabled, but not able to get an OpenTelemetry tracer. "
                        "Please ensure that `opentelemetry-api` is installed."
                    )
                    return

                otel_span = tracer.start_span(
                    name=span_name,
                    kind=SpanKind.CLIENT,
                    attributes=span_attributes,
                )

                with tracer.use_span(otel_span, end_on_exit=False):
                    trace_context_headers = tracer.get_trace_context()
                    request.http_request.headers.update(trace_context_headers)

                request.context[self.TRACING_CONTEXT] = otel_span
                token = tracer._suppress_auto_http_instrumentation()  # pylint: disable=protected-access
                request.context[self._SUPPRESSION_TOKEN] = token

        except Exception:  # pylint: disable=broad-except
            _LOGGER.warning("Unable to start network span.")

    def end_span(
        self,
        request: PipelineRequest[HTTPRequestType],
        response: Optional[HTTPResponseType] = None,
        exc_info: Optional[OptExcInfo] = None,
    ) -> None:
        """Ends the span that is tracing the network and updates its status.

        :param request: The PipelineRequest object
        :type request: ~azure.core.pipeline.PipelineRequest
        :param response: The HttpResponse object
        :type response: ~azure.core.rest.HTTPResponse or ~azure.core.pipeline.transport.HttpResponse
        :param exc_info: The exception information
        :type exc_info: tuple
        """
        if self.TRACING_CONTEXT not in request.context:
            return

        span = request.context[self.TRACING_CONTEXT]
        if not span:
            return

        http_request: Union[HttpRequest, LegacyHttpRequest] = request.http_request

        attributes: Dict[str, Any] = {}
        if request.context.get("retry_count"):
            attributes[self._HTTP_RESEND_COUNT] = request.context["retry_count"]
        if http_request.headers.get(self._REQUEST_ID):
            attributes[self._REQUEST_ID_ATTR] = http_request.headers[self._REQUEST_ID]
        if response and self._RESPONSE_ID in response.headers:
            attributes[self._RESPONSE_ID_ATTR] = response.headers[self._RESPONSE_ID]

        # We'll determine if the span is from a plugin or the core tracing library based on the presence of the
        # `set_http_attributes` method.
        if hasattr(span, "set_http_attributes"):
            # Plugin-based tracing
            span.set_http_attributes(request=http_request, response=response)
            for key, value in attributes.items():
                span.add_attribute(key, value)
            if exc_info:
                span.__exit__(*exc_info)
            else:
                span.finish()
        else:
            # Native tracing
            self._set_http_client_span_attributes(span, request=http_request, response=response)
            span.set_attributes(attributes)
            if exc_info:
                # If there was an exception, set the error.type attribute.
                exception_type = exc_info[0]
                if exception_type:
                    module = exception_type.__module__ if exception_type.__module__ != "builtins" else ""
                    error_type = f"{module}.{exception_type.__qualname__}" if module else exception_type.__qualname__
                    span.set_attribute(self._ERROR_TYPE, error_type)

                span.__exit__(*exc_info)
            else:
                span.end()

        suppression_token = request.context.get(self._SUPPRESSION_TOKEN)
        if suppression_token:
            tracer = get_tracer()
            if tracer:
                tracer._detach_from_context(suppression_token)  # pylint: disable=protected-access

    def on_response(
        self,
        request: PipelineRequest[HTTPRequestType],
        response: PipelineResponse[HTTPRequestType, HTTPResponseType],
    ) -> None:
        """Ends the span for the network call and updates its status.

        :param request: The PipelineRequest object
        :type request: ~azure.core.pipeline.PipelineRequest
        :param response: The PipelineResponse object
        :type response: ~azure.core.pipeline.PipelineResponse
        """
        self.end_span(request, response=response.http_response)

    def on_exception(self, request: PipelineRequest[HTTPRequestType]) -> None:
        """Ends the span for the network call and updates its status with exception info.

        :param request: The PipelineRequest object
        :type request: ~azure.core.pipeline.PipelineRequest
        """
        self.end_span(request, exc_info=sys.exc_info())

    def _set_http_client_span_attributes(
        self,
        span: "Span",
        request: Union[HttpRequest, LegacyHttpRequest],
        response: Optional[HTTPResponseType] = None,
    ) -> None:
        """Add attributes to an HTTP client span.

        :param span: The span to add attributes to.
        :type span: ~opentelemetry.trace.Span
        :param request: The request made
        :type request: ~azure.core.rest.HttpRequest
        :param response: The response received from the server. Is None if no response received.
        :type response: ~azure.core.rest.HTTPResponse or ~azure.core.pipeline.transport.HttpResponse
        """
        attributes: Dict[str, Any] = {
            self._HTTP_REQUEST_METHOD: request.method,
            self._URL_FULL: request.url,
        }

        parsed_url = urllib.parse.urlparse(request.url)
        if parsed_url.hostname:
            attributes[self._SERVER_ADDRESS] = parsed_url.hostname
        if parsed_url.port:
            attributes[self._SERVER_PORT] = parsed_url.port

        user_agent = request.headers.get("User-Agent")
        if user_agent:
            attributes[self._USER_AGENT_ORIGINAL] = user_agent
        if response and response.status_code:
            attributes[self._HTTP_RESPONSE_STATUS_CODE] = response.status_code
            if response.status_code >= 400:
                attributes[self._ERROR_TYPE] = str(response.status_code)

        span.set_attributes(attributes)

# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# --------------------------------------------------------------------------

from ._base import HTTPPolicy, SansIOHTTPPolicy, RequestHistory
from ._authentication import (
    BearerTokenCredentialPolicy,
    ServiceKeyCredentialPolicy,
)
from ._distributed_tracing import DistributedHttpTracingPolicy
from ._retry import RetryPolicy, RetryMode
from ._universal import (
    HeadersPolicy,
    UserAgentPolicy,
    NetworkTraceLoggingPolicy,
    ContentDecodePolicy,
    ProxyPolicy,
)
from ._base_async import AsyncHTTPPolicy
from ._authentication_async import AsyncBearerTokenCredentialPolicy
from ._retry_async import AsyncRetryPolicy

__all__ = [
    "HTTPPolicy",
    "SansIOHTTPPolicy",
    "BearerTokenCredentialPolicy",
    "ServiceKeyCredentialPolicy",
    "HeadersPolicy",
    "UserAgentPolicy",
    "NetworkTraceLoggingPolicy",
    "ContentDecodePolicy",
    "RetryMode",
    "RetryPolicy",
    "ProxyPolicy",
    "RequestHistory",
    "AsyncHTTPPolicy",
    "AsyncBearerTokenCredentialPolicy",
    "AsyncRetryPolicy",
    "DistributedHttpTracingPolicy",
]

# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import logging
import os
import sys
from typing import TYPE_CHECKING, Any

from ._constants import CACHE_CAE_SUFFIX, CACHE_NON_CAE_SUFFIX

if TYPE_CHECKING:
    import msal_extensions

_LOGGER = logging.getLogger(__name__)


class TokenCachePersistenceOptions:
    """Options for persistent token caching.

    Most credentials accept an instance of this class to configure persistent token caching. The default values
    configure a credential to use a cache shared with Microsoft developer tools and
    :class:`~azure.identity.SharedTokenCacheCredential`. To isolate a credential's data from other applications,
    specify a `name` for the cache.

    By default, the cache is encrypted with the current platform's user data protection API, and will raise an error
    when this is not available. To configure the cache to fall back to an unencrypted file instead of raising an
    error, specify `allow_unencrypted_storage=True`.

    .. warning:: The cache contains authentication secrets. If the cache is not encrypted, protecting it is the
       application's responsibility. A breach of its contents will fully compromise accounts.

    .. admonition:: Example:

        .. literalinclude:: ../tests/test_persistent_cache.py
            :start-after: [START snippet]
            :end-before: [END snippet]
            :language: python
            :caption: Configuring a credential for persistent caching
            :dedent: 8

    :keyword str name: prefix name of the cache, used to isolate its data from other applications. Defaults to the
        name of the cache shared by Microsoft dev tools and :class:`~azure.identity.SharedTokenCacheCredential`.
        Additional strings may be appended to the name for further isolation.
    :keyword bool allow_unencrypted_storage: whether the cache should fall back to storing its data in plain text when
        encryption isn't possible. False by default. Setting this to True does not disable encryption. The cache will
        always try to encrypt its data.
    """

    def __init__(self, *, allow_unencrypted_storage: bool = False, name: str = "msal.cache", **kwargs: Any) -> None:
        # pylint:disable=unused-argument
        self.allow_unencrypted_storage = allow_unencrypted_storage
        self.name = name


def _load_persistent_cache(
    options: TokenCachePersistenceOptions, is_cae: bool = False
) -> "msal_extensions.PersistedTokenCache":
    import msal_extensions

    cache_suffix = CACHE_CAE_SUFFIX if is_cae else CACHE_NON_CAE_SUFFIX
    persistence = _get_persistence(
        allow_unencrypted=options.allow_unencrypted_storage,
        account_name="MSALCache",
        cache_name=options.name + cache_suffix,
    )
    return msal_extensions.PersistedTokenCache(persistence)


def _get_persistence(
    allow_unencrypted: bool, account_name: str, cache_name: str
) -> "msal_extensions.persistence.BasePersistence":
    """Get an msal_extensions persistence instance for the current platform.

    On Windows the cache is a file protected by the Data Protection API. On Linux and macOS the cache is stored by
    libsecret and Keychain, respectively. On those platforms the cache uses the modified timestamp of a file on disk to
    decide whether to reload the cache.

    :param bool allow_unencrypted: when True, the cache will be kept in plaintext should encryption be impossible in the
        current environment
    :param str account_name: the name of the account for which the cache is storing tokens
    :param str cache_name: the name of the cache
    :return: an msal_extensions persistence instance
    :rtype: ~msal_extensions.persistence.BasePersistence
    """
    import msal_extensions

    if sys.platform.startswith("win") and "LOCALAPPDATA" in os.environ:
        cache_location = os.path.join(os.environ["LOCALAPPDATA"], ".IdentityService", cache_name)
        return msal_extensions.FilePersistenceWithDataProtection(cache_location)

    if sys.platform.startswith("darwin"):
        # the cache uses this file's modified timestamp to decide whether to reload
        file_path = os.path.expanduser(os.path.join("~", ".IdentityService", cache_name))
        return msal_extensions.KeychainPersistence(file_path, "Microsoft.Developer.IdentityService", account_name)

    if sys.platform.startswith("linux"):
        # The cache uses this file's modified timestamp to decide whether to reload. Note this path is the same
        # as that of the plaintext fallback: a new encrypted cache will stomp an unencrypted cache.
        file_path = os.path.expanduser(os.path.join("~", ".IdentityService", cache_name))
        try:
            return msal_extensions.LibsecretPersistence(
                file_path, cache_name, {"MsalClientID": "Microsoft.Developer.IdentityService"}, label=account_name
            )
        except Exception as ex:  # pylint:disable=broad-except
            _LOGGER.debug('msal-extensions is unable to encrypt a persistent cache: "%s"', ex, exc_info=True)
            if not allow_unencrypted:
                error = ValueError(
                    "Cache encryption is impossible because libsecret dependencies are not installed or are unusable,"
                    + " for example because no display is available (as in an SSH session). The chained exception has"
                    + ' more information. Specify "allow_unencrypted_storage=True" to store the cache unencrypted'
                    + " instead of raising this exception."
                )
                raise error from ex
        return msal_extensions.FilePersistence(file_path)

    raise NotImplementedError("A persistent cache is not available in this environment.")

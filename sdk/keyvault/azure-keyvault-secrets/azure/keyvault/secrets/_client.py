# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
from datetime import datetime
from functools import partial
from typing import Any, cast, Dict, Optional

from azure.core.paging import ItemPaged
from azure.core.polling import LROPoller
from azure.core.tracing.decorator import distributed_trace

from ._models import KeyVaultSecret, DeletedSecret, SecretProperties
from ._shared import KeyVaultClientBase
from ._shared._polling import DeleteRecoverPollingMethod, KeyVaultOperationPoller


class SecretClient(KeyVaultClientBase):
    """A high-level interface for managing a vault's secrets.

    :param str vault_url: URL of the vault the client will access. This is also called the vault's "DNS Name".
        You should validate that this URL references a valid Key Vault resource. See https://aka.ms/azsdk/blog/vault-uri
        for details.
    :param credential: An object which can provide an access token for the vault, such as a credential from
        :mod:`azure.identity`
    :type credential: ~azure.core.credentials.TokenCredential

    :keyword api_version: Version of the service API to use. Defaults to the most recent.
    :paramtype api_version: ~azure.keyvault.secrets.ApiVersion or str
    :keyword bool verify_challenge_resource: Whether to verify the authentication challenge resource matches the Key
        Vault domain. Defaults to True.

    Example:
        .. literalinclude:: ../tests/test_samples_secrets.py
            :start-after: [START create_secret_client]
            :end-before: [END create_secret_client]
            :language: python
            :caption: Create a new ``SecretClient``
            :dedent: 4
    """

    # pylint:disable=protected-access

    @distributed_trace
    def get_secret(self, name: str, version: Optional[str] = None, **kwargs: Any) -> KeyVaultSecret:
        """Get a secret. Requires the secrets/get permission.

        :param str name: The name of the secret
        :param str version: (optional) Version of the secret to get. If unspecified, gets the latest version.

        :returns: The fetched secret.
        :rtype: ~azure.keyvault.secrets.KeyVaultSecret

        :raises ~azure.core.exceptions.ResourceNotFoundError or ~azure.core.exceptions.HttpResponseError:
            the former if the secret doesn't exist; the latter for other errors

        Example:
            .. literalinclude:: ../tests/test_samples_secrets.py
                :start-after: [START get_secret]
                :end-before: [END get_secret]
                :language: python
                :caption: Get a secret
                :dedent: 8
        """
        bundle = self._client.get_secret(
            secret_name=name,
            secret_version=version or "",
            **kwargs
        )
        return KeyVaultSecret._from_secret_bundle(bundle)

    @distributed_trace
    def set_secret(
        self,
        name: str,
        value: str,
        *,
        enabled: Optional[bool] = None,
        tags: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = None,
        not_before: Optional[datetime] = None,
        expires_on: Optional[datetime] = None,
        **kwargs: Any,
    ) -> KeyVaultSecret:
        """Set a secret value. If `name` is in use, create a new version of the secret. If not, create a new secret.

        Requires secrets/set permission.

        :param str name: The name of the secret
        :param str value: The value of the secret

        :keyword bool enabled: Whether the secret is enabled for use.
        :keyword tags: Application specific metadata in the form of key-value pairs.
        :paramtype tags: Dict[str, str] or None
        :keyword str content_type: An arbitrary string indicating the type of the secret, e.g. 'password'
        :keyword ~datetime.datetime not_before: Not before date of the secret in UTC
        :keyword ~datetime.datetime expires_on: Expiry date of the secret in UTC

        :returns: The created or updated secret.
        :rtype: ~azure.keyvault.secrets.KeyVaultSecret

        :raises ~azure.core.exceptions.HttpResponseError:

        Example:
            .. literalinclude:: ../tests/test_samples_secrets.py
                :start-after: [START set_secret]
                :end-before: [END set_secret]
                :language: python
                :caption: Set a secret's value
                :dedent: 8

        """
        if enabled is not None or not_before is not None or expires_on is not None:
            attributes = self._models.SecretAttributes(
                enabled=enabled, not_before=not_before, expires=expires_on
            )
        else:
            attributes = None

        parameters = self._models.SecretSetParameters(
            value=value,
            tags=tags,
            content_type=content_type,
            secret_attributes=attributes
        )

        bundle = self._client.set_secret(
            secret_name=name,
            parameters=parameters,
            **kwargs
        )
        return KeyVaultSecret._from_secret_bundle(bundle)

    @distributed_trace
    def update_secret_properties(
        self,
        name: str,
        version: Optional[str] = None,
        *,
        enabled: Optional[bool] = None,
        tags: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = None,
        not_before: Optional[datetime] = None,
        expires_on: Optional[datetime] = None,
        **kwargs: Any,
    ) -> SecretProperties:
        """Update properties of a secret other than its value. Requires secrets/set permission.

        This method updates properties of the secret, such as whether it's enabled, but can't change the secret's
        value. Use :func:`set_secret` to change the secret's value.

        :param str name: Name of the secret
        :param str version: (optional) Version of the secret to update. If unspecified, the latest version is updated.

        :keyword bool enabled: Whether the secret is enabled for use.
        :keyword tags: Application specific metadata in the form of key-value pairs.
        :paramtype tags: Dict[str, str] or None
        :keyword str content_type: An arbitrary string indicating the type of the secret, e.g. 'password'
        :keyword ~datetime.datetime not_before: Not before date of the secret in UTC
        :keyword ~datetime.datetime expires_on: Expiry date of the secret in UTC

        :returns: The updated secret properties.
        :rtype: ~azure.keyvault.secrets.SecretProperties

        :raises ~azure.core.exceptions.ResourceNotFoundError or ~azure.core.exceptions.HttpResponseError:
            the former if the secret doesn't exist; the latter for other errors

        Example:
            .. literalinclude:: ../tests/test_samples_secrets.py
                :start-after: [START update_secret]
                :end-before: [END update_secret]
                :language: python
                :caption: Update a secret's attributes
                :dedent: 8

        """
        if enabled is not None or not_before is not None or expires_on is not None:
            attributes = self._models.SecretAttributes(
                enabled=enabled, not_before=not_before, expires=expires_on
            )
        else:
            attributes = None

        parameters = self._models.SecretUpdateParameters(
            content_type=content_type,
            secret_attributes=attributes,
            tags=tags,
        )

        bundle = self._client.update_secret(
            name,
            secret_version=version or "",
            parameters=parameters,
            **kwargs
        )
        return SecretProperties._from_secret_bundle(bundle)  # pylint: disable=protected-access

    @distributed_trace
    def list_properties_of_secrets(self, **kwargs: Any) -> ItemPaged[SecretProperties]:
        """List identifiers and attributes of all secrets in the vault. Requires secrets/list permission.

        List items don't include secret values. Use :func:`get_secret` to get a secret's value.

        :returns: An iterator of secrets, excluding their values
        :rtype: ~azure.core.paging.ItemPaged[~azure.keyvault.secrets.SecretProperties]

        Example:
            .. literalinclude:: ../tests/test_samples_secrets.py
                :start-after: [START list_secrets]
                :end-before: [END list_secrets]
                :language: python
                :caption: List all secrets
                :dedent: 8

        """
        return self._client.get_secrets(
            maxresults=kwargs.pop("max_page_size", None),
            cls=lambda objs: [SecretProperties._from_secret_item(x) for x in objs],
            **kwargs
        )

    @distributed_trace
    def list_properties_of_secret_versions(self, name: str, **kwargs: Any) -> ItemPaged[SecretProperties]:
        """List properties of all versions of a secret, excluding their values. Requires secrets/list permission.

        List items don't include secret values. Use :func:`get_secret` to get a secret's value.

        :param str name: Name of the secret

        :returns: An iterator of secrets, excluding their values
        :rtype: ~azure.core.paging.ItemPaged[~azure.keyvault.secrets.SecretProperties]

        Example:
            .. literalinclude:: ../tests/test_samples_secrets.py
                :start-after: [START list_properties_of_secret_versions]
                :end-before: [END list_properties_of_secret_versions]
                :language: python
                :caption: List all versions of a secret
                :dedent: 8

        """
        return self._client.get_secret_versions(
            name,
            maxresults=kwargs.pop("max_page_size", None),
            cls=lambda objs: [SecretProperties._from_secret_item(x) for x in objs],
            **kwargs
        )

    @distributed_trace
    def backup_secret(self, name: str, **kwargs: Any) -> bytes:
        """Back up a secret in a protected form useable only by Azure Key Vault. Requires secrets/backup permission.

        :param str name: Name of the secret to back up

        :returns: The backup result, in a protected bytes format that can only be used by Azure Key Vault.
        :rtype: bytes

        :raises ~azure.core.exceptions.ResourceNotFoundError or ~azure.core.exceptions.HttpResponseError:
            the former if the secret doesn't exist; the latter for other errors

        Example:
            .. literalinclude:: ../tests/test_samples_secrets.py
                :start-after: [START backup_secret]
                :end-before: [END backup_secret]
                :language: python
                :caption: Back up a secret
                :dedent: 8

        """
        backup_result = self._client.backup_secret(name, **kwargs)
        return cast(bytes, backup_result.value)

    @distributed_trace
    def restore_secret_backup(self, backup: bytes, **kwargs: Any) -> SecretProperties:
        """Restore a backed up secret. Requires the secrets/restore permission.

        :param bytes backup: A secret backup as returned by :func:`backup_secret`

        :returns: The restored secret
        :rtype: ~azure.keyvault.secrets.SecretProperties

        :raises ~azure.core.exceptions.ResourceExistsError or ~azure.core.exceptions.HttpResponseError:
            the former if the secret's name is already in use; the latter for other errors

        Example:
            .. literalinclude:: ../tests/test_samples_secrets.py
                :start-after: [START restore_secret_backup]
                :end-before: [END restore_secret_backup]
                :language: python
                :caption: Restore a backed up secret
                :dedent: 8

        """
        bundle = self._client.restore_secret(
            parameters=self._models.SecretRestoreParameters(secret_bundle_backup=backup),
            **kwargs
        )
        return SecretProperties._from_secret_bundle(bundle)

    @distributed_trace
    def begin_delete_secret(self, name: str, **kwargs: Any) -> LROPoller[DeletedSecret]:  # pylint:disable=bad-option-value,delete-operation-wrong-return-type
        """Delete all versions of a secret. Requires secrets/delete permission.

        When this method returns Key Vault has begun deleting the secret. Deletion may take several seconds in a vault
        with soft-delete enabled. This method therefore returns a poller enabling you to wait for deletion to complete.

        :param str name: Name of the secret to delete.

        :returns: A poller for the delete operation. The poller's `result` method returns the
            :class:`~azure.keyvault.secrets.DeletedSecret` without waiting for deletion to complete. If the vault has
            soft-delete enabled and you want to permanently delete the secret with :func:`purge_deleted_secret`, call
            the poller's `wait` method first. It will block until the deletion is complete. The `wait` method requires
            secrets/get permission.
        :rtype: ~azure.core.polling.LROPoller[~azure.keyvault.secrets.DeletedSecret]

        :raises ~azure.core.exceptions.ResourceNotFoundError or ~azure.core.exceptions.HttpResponseError:
            the former if the secret doesn't exist; the latter for other errors

        Example:
            .. literalinclude:: ../tests/test_samples_secrets.py
                :start-after: [START delete_secret]
                :end-before: [END delete_secret]
                :language: python
                :caption: Delete a secret
                :dedent: 8

        """
        polling_interval = kwargs.pop("_polling_interval", None)
        if polling_interval is None:
            polling_interval = 2
        # Ignore pyright warning about return type not being iterable because we use `cls` to return a tuple
        pipeline_response, deleted_secret_bundle = self._client.delete_secret(
            secret_name=name,
            cls=lambda pipeline_response, deserialized, _: (pipeline_response, deserialized),
            **kwargs,
        )  # pyright: ignore[reportGeneralTypeIssues]
        deleted_secret = DeletedSecret._from_deleted_secret_bundle(deleted_secret_bundle)

        command = partial(self.get_deleted_secret, name=name, **kwargs)
        polling_method = DeleteRecoverPollingMethod(
            # no recovery ID means soft-delete is disabled, in which case we initialize the poller as finished
            finished=deleted_secret.recovery_id is None,
            pipeline_response=pipeline_response,
            command=command,
            final_resource=deleted_secret,
            interval=polling_interval,
        )
        return KeyVaultOperationPoller(polling_method)

    @distributed_trace
    def get_deleted_secret(self, name: str, **kwargs: Any) -> DeletedSecret:
        """Get a deleted secret. Possible only in vaults with soft-delete enabled. Requires secrets/get permission.

        :param str name: Name of the deleted secret

        :returns: The deleted secret.
        :rtype: ~azure.keyvault.secrets.DeletedSecret

        :raises ~azure.core.exceptions.ResourceNotFoundError or ~azure.core.exceptions.HttpResponseError:
            the former if the deleted secret doesn't exist; the latter for other errors

        Example:
            .. literalinclude:: ../tests/test_samples_secrets.py
                :start-after: [START get_deleted_secret]
                :end-before: [END get_deleted_secret]
                :language: python
                :caption: Get a deleted secret
                :dedent: 8

        """
        bundle = self._client.get_deleted_secret(name, **kwargs)
        return DeletedSecret._from_deleted_secret_bundle(bundle)

    @distributed_trace
    def list_deleted_secrets(self, **kwargs: Any) -> ItemPaged[DeletedSecret]:
        """Lists all deleted secrets. Possible only in vaults with soft-delete enabled.

        Requires secrets/list permission.

        :returns: An iterator of deleted secrets, excluding their values
        :rtype: ~azure.core.paging.ItemPaged[~azure.keyvault.secrets.DeletedSecret]

        Example:
            .. literalinclude:: ../tests/test_samples_secrets.py
                :start-after: [START list_deleted_secrets]
                :end-before: [END list_deleted_secrets]
                :language: python
                :caption: List deleted secrets
                :dedent: 8

        """
        return self._client.get_deleted_secrets(
            maxresults=kwargs.pop("max_page_size", None),
            cls=lambda objs: [DeletedSecret._from_deleted_secret_item(x) for x in objs],
            **kwargs
        )

    @distributed_trace
    def purge_deleted_secret(self, name: str, **kwargs: Any) -> None:
        """Permanently deletes a deleted secret. Possible only in vaults with soft-delete enabled.

        Performs an irreversible deletion of the specified secret, without possibility for recovery. The operation is
        not available if the :py:attr:`~azure.keyvault.secrets.SecretProperties.recovery_level` does not specify
        'Purgeable'. This method is only necessary for purging a secret before its
        :py:attr:`~azure.keyvault.secrets.DeletedSecret.scheduled_purge_date`.

        Requires secrets/purge permission.

        :param str name: Name of the deleted secret to purge

        :returns: None

        :raises ~azure.core.exceptions.HttpResponseError:

        Example:
            .. code-block:: python

                # if the vault has soft-delete enabled, purge permanently deletes the secret
                # (with soft-delete disabled, begin_delete_secret is permanent)
                secret_client.purge_deleted_secret("secret-name")

        """
        self._client.purge_deleted_secret(name, **kwargs)

    @distributed_trace
    def begin_recover_deleted_secret(self, name: str, **kwargs: Any) -> LROPoller[SecretProperties]:
        """Recover a deleted secret to its latest version. Possible only in a vault with soft-delete enabled.

        Requires the secrets/recover permission. If the vault does not have soft-delete enabled,
        :func:`begin_delete_secret` is permanent, and this method will return an error. Attempting to recover a
        non-deleted secret will also return an error. When this method returns Key Vault has begun recovering the
        secret. Recovery may take several seconds. This method therefore returns a poller enabling you to wait for
        recovery to complete. Waiting is only necessary when you want to use the recovered secret in another operation
        immediately.

        :param str name: Name of the deleted secret to recover

        :returns: A poller for the recovery operation. The poller's `result` method returns the recovered secret's
            :class:`~azure.keyvault.secrets.SecretProperties` without waiting for recovery to complete. If you want to
            use the recovered secret immediately, call the poller's `wait` method, which blocks until the secret is
            ready to use. The `wait` method requires secrets/get permission.
        :rtype: ~azure.core.polling.LROPoller[~azure.keyvault.secrets.SecretProperties]

        :raises ~azure.core.exceptions.HttpResponseError:

        Example:
            .. literalinclude:: ../tests/test_samples_secrets.py
                :start-after: [START recover_deleted_secret]
                :end-before: [END recover_deleted_secret]
                :language: python
                :caption: Recover a deleted secret
                :dedent: 8

        """
        polling_interval = kwargs.pop("_polling_interval", None)
        if polling_interval is None:
            polling_interval = 2
        # Ignore pyright warning about return type not being iterable because we use `cls` to return a tuple
        pipeline_response, recovered_secret_bundle = self._client.recover_deleted_secret(
            secret_name=name,
            cls=lambda pipeline_response, deserialized, _: (pipeline_response, deserialized),
            **kwargs,
        )  # pyright: ignore[reportGeneralTypeIssues]
        recovered_secret = SecretProperties._from_secret_bundle(recovered_secret_bundle)

        command = partial(self.get_secret, name=name, **kwargs)
        polling_method = DeleteRecoverPollingMethod(
            finished=False,
            pipeline_response=pipeline_response,
            command=command,
            final_resource=recovered_secret,
            interval=polling_interval,
        )
        return KeyVaultOperationPoller(polling_method)

    def __enter__(self) -> "SecretClient":
        self._client.__enter__()
        return self

# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# -------------------------------------
from collections import namedtuple
from datetime import datetime
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

from ._enums import KeyOperation, KeyRotationPolicyAction, KeyType
from ._shared import parse_key_vault_id
from ._generated.models import JsonWebKey as _JsonWebKey

if TYPE_CHECKING:
    from ._generated import models as _models

KeyOperationResult = namedtuple("KeyOperationResult", ["id", "value"])


class JsonWebKey(object):
    """As defined in http://tools.ietf.org/html/draft-ietf-jose-json-web-key-18. All parameters are optional.

    :keyword str kid: Key identifier.
    :keyword kty: Key Type (kty), as defined in https://tools.ietf.org/html/draft-ietf-jose-json-web-algorithms-40
    :paramtype kty: ~azure.keyvault.keys.KeyType or str
    :keyword key_ops: Allowed operations for the key
    :paramtype key_ops: list[str or ~azure.keyvault.keys.KeyOperation]
    :keyword bytes n: RSA modulus.
    :keyword bytes e: RSA public exponent.
    :keyword bytes d: RSA private exponent, or the D component of an EC private key.
    :keyword bytes dp: RSA private key parameter.
    :keyword bytes dq: RSA private key parameter.
    :keyword bytes qi: RSA private key parameter.
    :keyword bytes p: RSA secret prime.
    :keyword bytes q: RSA secret prime, with p < q.
    :keyword bytes k: Symmetric key.
    :keyword bytes t: HSM Token, used with 'Bring Your Own Key'.
    :keyword crv: Elliptic curve name.
    :paramtype crv: ~azure.keyvault.keys.KeyCurveName or str
    :keyword bytes x: X component of an EC public key.
    :keyword bytes y: Y component of an EC public key.
    """

    _FIELDS = ("kid", "kty", "key_ops", "n", "e", "d", "dp", "dq", "qi", "p", "q", "k", "t", "crv", "x", "y")

    def __init__(self, **kwargs: Any) -> None:
        for field in self._FIELDS:
            setattr(self, field, kwargs.get(field))

    def _to_generated_model(self) -> _JsonWebKey:
        jwk = _JsonWebKey()
        for field in self._FIELDS:
            setattr(jwk, field, getattr(self, field))
        return jwk


class KeyAttestation:
    """The key attestation information.

    :ivar certificate_pem_file: The certificate used for attestation validation, in PEM format.
    :vartype certificate_pem_file: bytes or None
    :ivar private_key_attestation: The key attestation corresponding to the private key material of the key.
    :vartype private_key_attestation: bytes or None
    :ivar public_key_attestation: The key attestation corresponding to the public key material of the key.
    :vartype public_key_attestation: bytes or None
    :ivar version: The version of the attestation.
    :vartype version: str or None
    """

    def __init__(
        self,
        *,
        certificate_pem_file: Optional[bytes] = None,
        private_key_attestation: Optional[bytes] = None,
        public_key_attestation: Optional[bytes] = None,
        version: Optional[str] = None,
    ) -> None:
        self.certificate_pem_file = certificate_pem_file
        self.private_key_attestation = private_key_attestation
        self.public_key_attestation = public_key_attestation
        self.version = version

    def __repr__(self) -> str:
        return f"<KeyAttestation [{self.version}]>"[:1024]

    @classmethod
    def _from_generated(cls, attestation: "_models.KeyAttestation") -> "KeyAttestation":
        return cls(
            certificate_pem_file=attestation.certificate_pem_file,
            private_key_attestation=attestation.private_key_attestation,
            public_key_attestation=attestation.public_key_attestation,
            version=attestation.version,
        )


class KeyProperties(object):
    """A key's ID and attributes.

    :param str key_id: The key ID.
    :param attributes: The key attributes.
    :type attributes: ~azure.keyvault.keys._generated.models.KeyAttributes

    :keyword bool managed: Whether the key's lifetime is managed by Key Vault.
    :keyword tags: Application specific metadata in the form of key-value pairs.
    :paramtype tags: dict[str, str] or None
    :keyword release_policy: The azure.keyvault.keys.KeyReleasePolicy specifying the rules under which the key
        can be exported.
    :paramtype release_policy: ~azure.keyvault.keys.KeyReleasePolicy or None
    """

    def __init__(self, key_id: str, attributes: "Optional[_models.KeyAttributes]" = None, **kwargs: Any) -> None:
        self._attributes = attributes
        self._id = key_id
        self._vault_id = KeyVaultKeyIdentifier(key_id)
        self._managed = kwargs.get("managed", None)
        self._tags = kwargs.get("tags", None)
        self._release_policy = kwargs.pop("release_policy", None)

    def __repr__(self) -> str:
        return f"<KeyProperties [{self.id}]>"[:1024]

    @classmethod
    def _from_key_bundle(cls, key_bundle: Union["_models.KeyBundle", "_models.DeletedKeyBundle"]) -> "KeyProperties":
        # pylint:disable=line-too-long
        # release_policy was added in 7.3-preview
        release_policy = None
        if (
            hasattr(key_bundle, "release_policy") and key_bundle.release_policy is not None  # type: ignore[attr-defined]
        ):
            release_policy = KeyReleasePolicy(
                encoded_policy=key_bundle.release_policy.encoded_policy,  # type: ignore
                content_type=key_bundle.release_policy.content_type,  # type: ignore[attr-defined]
                immutable=key_bundle.release_policy.immutable,  # type: ignore[attr-defined]
            )

        return cls(
            key_bundle.key.kid,  # type: ignore
            attributes=key_bundle.attributes,
            managed=key_bundle.managed,
            tags=key_bundle.tags,
            release_policy=release_policy,
        )

    @classmethod
    def _from_key_item(cls, key_item: Union["_models.KeyItem", "_models.DeletedKeyItem"]) -> "KeyProperties":
        return cls(
            key_id=key_item.kid,  # type: ignore
            attributes=key_item.attributes,
            managed=key_item.managed,
            tags=key_item.tags,
        )

    @property
    def id(self) -> str:
        """The key ID.

        :returns: The key ID.
        :rtype: str
        """
        return self._id

    @property
    def name(self) -> str:
        """The key name.

        :returns: The key name.
        :rtype: str
        """
        return self._vault_id.name

    @property
    def version(self) -> Optional[str]:
        """The key version.

        :returns: The key version.
        :rtype: str or None
        """
        return self._vault_id.version

    @property
    def enabled(self) -> Optional[bool]:
        """Whether the key is enabled for use.

        :returns: True if the key is enabled for use; False otherwise.
        :rtype: bool or None
        """
        return self._attributes.enabled if self._attributes else None

    @property
    def not_before(self) -> Optional[datetime]:
        """The time before which the key can not be used, in UTC.

        :returns: The time before which the key can not be used, in UTC.
        :rtype: ~datetime.datetime or None
        """
        return self._attributes.not_before if self._attributes else None

    @property
    def expires_on(self) -> Optional[datetime]:
        """When the key will expire, in UTC.

        :returns: When the key will expire, in UTC.
        :rtype: ~datetime.datetime or None
        """
        return self._attributes.expires if self._attributes else None

    @property
    def created_on(self) -> Optional[datetime]:
        """When the key was created, in UTC.

        :returns: When the key was created, in UTC.
        :rtype: ~datetime.datetime or None
        """
        return self._attributes.created if self._attributes else None

    @property
    def updated_on(self) -> Optional[datetime]:
        """When the key was last updated, in UTC.

        :returns: When the key was last updated, in UTC.
        :rtype: ~datetime.datetime or None
        """
        return self._attributes.updated if self._attributes else None

    @property
    def vault_url(self) -> str:
        """URL of the vault containing the key.

        :returns: URL of the vault containing the key.
        :rtype: str
        """
        return self._vault_id.vault_url

    @property
    def recoverable_days(self) -> Optional[int]:
        """The number of days the key is retained before being deleted from a soft-delete enabled Key Vault.

        :returns: The number of days the key is retained before being deleted from a soft-delete enabled Key Vault.
        :rtype: int or None
        """
        # recoverable_days was added in 7.1-preview
        if self._attributes:
            return getattr(self._attributes, "recoverable_days", None)
        return None

    @property
    def recovery_level(self) -> Optional[str]:
        """The vault's deletion recovery level for keys.

        :returns: The vault's deletion recovery level for keys.
        :rtype: str or None
        """
        return self._attributes.recovery_level if self._attributes else None

    @property
    def tags(self) -> Dict[str, str]:
        """Application specific metadata in the form of key-value pairs.

        :returns: A dictionary of tags attached to the key.
        :rtype: dict[str, str]
        """
        return self._tags

    @property
    def managed(self) -> Optional[bool]:
        """Whether the key's lifetime is managed by Key Vault. If the key backs a certificate, this will be true.

        :returns: True if the key's lifetime is managed by Key Vault; False otherwise.
        :rtype: bool or None
        """
        return self._managed

    @property
    def exportable(self) -> Optional[bool]:
        """Whether the private key can be exported.

        :returns: True if the private key can be exported; False otherwise.
        :rtype: bool or None
        """
        # exportable was added in 7.3-preview
        if self._attributes:
            return getattr(self._attributes, "exportable", None)
        return None

    @property
    def release_policy(self) -> "Optional[KeyReleasePolicy]":
        """The :class:`~azure.keyvault.keys.KeyReleasePolicy` specifying the rules under which the key can be exported.

        :returns: The key's release policy specifying the rules for exporting.
        :rtype: ~azure.keyvault.keys.KeyReleasePolicy or None
        """
        return self._release_policy

    @property
    def hsm_platform(self) -> Optional[str]:
        """The underlying HSM platform.

        :returns: The underlying HSM platform.
        :rtype: str or None
        """
        # hsm_platform was added in 7.5-preview.1
        if self._attributes:
            return getattr(self._attributes, "hsm_platform", None)
        return None

    @property
    def attestation(self) -> Optional[KeyAttestation]:
        """The key attestation, if available and requested.

        :returns: The key or key version attestation information.
        :rtype: ~azure.keyvault.keys.KeyAttestation or None
        """
        # attestation was added in 7.6-preview.2
        if self._attributes:
            attestation = getattr(self._attributes, "attestation", None)
            return KeyAttestation._from_generated(attestation=attestation) if attestation else None  # pylint:disable=protected-access
        return None


class KeyReleasePolicy(object):
    """The policy rules under which a key can be exported.

    :param bytes encoded_policy: The policy rules under which the key can be released. Encoded based on the
        ``content_type``. For more information regarding release policy grammar, please refer to:
        https://aka.ms/policygrammarkeys for Azure Key Vault; https://aka.ms/policygrammarmhsm for Azure Managed HSM.

    :keyword str content_type: Content type and version of the release policy. Defaults to "application/json;
        charset=utf-8" if omitted.
    :keyword bool immutable: Marks a release policy as immutable. An immutable release policy cannot be changed or
        updated after being marked immutable. Release policies are mutable by default.
    """

    def __init__(self, encoded_policy: bytes, **kwargs: Any) -> None:
        self.encoded_policy = encoded_policy
        self.content_type = kwargs.get("content_type", None)
        self.immutable = kwargs.get("immutable", None)


class ReleaseKeyResult(object):
    """The result of a key release operation.

    :ivar str value: A signed token containing the released key.

    :param str value: A signed token containing the released key.
    """

    def __init__(self, value: str) -> None:
        self.value = value


class KeyRotationLifetimeAction(object):
    """An action and its corresponding trigger that will be performed by Key Vault over the lifetime of a key.

    :param action: The action that will be executed.
    :type action: ~azure.keyvault.keys.KeyRotationPolicyAction or str

    :keyword time_after_create: Time after creation to attempt the specified action, as an ISO 8601 duration.
        For example, 90 days is "P90D". See `Wikipedia <https://wikipedia.org/wiki/ISO_8601#Durations>`_ for more
        information on ISO 8601 durations.
    :paramtype time_after_create: str or None
    :keyword time_before_expiry: Time before expiry to attempt the specified action, as an ISO 8601 duration.
        For example, 90 days is "P90D". See `Wikipedia <https://wikipedia.org/wiki/ISO_8601#Durations>`_ for more
        information on ISO 8601 durations.
    :paramtype time_before_expiry: str or None
    """

    def __init__(self, action: Union[KeyRotationPolicyAction, str], **kwargs: Any) -> None:
        self.action = action
        self.time_after_create: Optional[str] = kwargs.get("time_after_create", None)
        self.time_before_expiry: Optional[str] = kwargs.get("time_before_expiry", None)

    @classmethod
    def _from_generated(cls, lifetime_action: "_models.LifetimeActions") -> "KeyRotationLifetimeAction":
        if lifetime_action.action:
            if lifetime_action.trigger:
                return cls(
                    action=lifetime_action.action.type,  # type: ignore
                    time_after_create=lifetime_action.trigger.time_after_create,
                    time_before_expiry=lifetime_action.trigger.time_before_expiry,
                )
            return cls(action=lifetime_action.action)  # type: ignore
        raise ValueError("Provided LifetimeActions model is missing a required lifetime action property.")


class KeyRotationPolicy(object):
    """The key rotation policy that belongs to a key.

    :ivar id: The identifier of the key rotation policy.
    :vartype id: str or None
    :ivar lifetime_actions: Actions that will be performed by Key Vault over the lifetime of a key.
    :vartype lifetime_actions: list[~azure.keyvault.keys.KeyRotationLifetimeAction]
    :ivar expires_in: The expiry time of the policy that will be applied on new key versions, defined as an ISO 8601
        duration. For example, 90 days is "P90D".  See `Wikipedia <https://wikipedia.org/wiki/ISO_8601#Durations>`_ for
        more information on ISO 8601 durations.
    :vartype expires_in: str or None
    :ivar created_on: When the policy was created, in UTC
    :vartype created_on: ~datetime.datetime or None
    :ivar updated_on: When the policy was last updated, in UTC
    :vartype updated_on: ~datetime.datetime or None
    """

    def __init__(self, **kwargs: Any) -> None:
        self.id = kwargs.get("policy_id", None)
        self.lifetime_actions: List[KeyRotationLifetimeAction] = kwargs.get("lifetime_actions", [])
        self.expires_in = kwargs.get("expires_in", None)
        self.created_on = kwargs.get("created_on", None)
        self.updated_on = kwargs.get("updated_on", None)

    @classmethod
    def _from_generated(cls, policy: "_models.KeyRotationPolicy") -> "KeyRotationPolicy":
        lifetime_actions = (
            []
            if policy.lifetime_actions is None
            else [
                KeyRotationLifetimeAction._from_generated(action) for action in policy.lifetime_actions  # pylint:disable=protected-access
            ]
        )
        if policy.attributes:
            return cls(
                policy_id=policy.id,
                lifetime_actions=lifetime_actions,
                expires_in=policy.attributes.expiry_time,
                created_on=policy.attributes.created,
                updated_on=policy.attributes.updated,
            )
        return cls(policy_id=policy.id, lifetime_actions=lifetime_actions)


class KeyVaultKey(object):
    """A key's attributes and cryptographic material.

    :param str key_id: Key Vault's identifier for the key. Typically a URI, e.g.
        https://myvault.vault.azure.net/keys/my-key/version
    :param jwk: The key's cryptographic material as a JSON Web Key (https://tools.ietf.org/html/rfc7517). This may be
        provided as a dictionary or keyword arguments. See :class:`~azure.keyvault.keys.models.JsonWebKey` for field
        names.
    :type jwk: Dict[str, Any]

    Providing cryptographic material as keyword arguments:

    .. code-block:: python

        from azure.keyvault.keys.models import KeyVaultKey

        key_id = 'https://myvault.vault.azure.net/keys/my-key/my-key-version'
        key_bytes = os.urandom(32)
        key = KeyVaultKey(key_id, k=key_bytes, kty='oct', key_ops=['unwrapKey', 'wrapKey'])

    Providing cryptographic material as a dictionary:

    .. code-block:: python

        from azure.keyvault.keys.models import KeyVaultKey

        key_id = 'https://myvault.vault.azure.net/keys/my-key/my-key-version'
        key_bytes = os.urandom(32)
        jwk = {'k': key_bytes, 'kty': 'oct', 'key_ops': ['unwrapKey', 'wrapKey']}
        key = KeyVaultKey(key_id, jwk=jwk)

    """

    def __init__(self, key_id: str, jwk: Optional[Dict[str, Any]] = None, **kwargs) -> None:
        self._properties: KeyProperties = kwargs.pop("properties", None) or KeyProperties(key_id, **kwargs)
        if isinstance(jwk, dict):
            if any(field in kwargs for field in JsonWebKey._FIELDS):
                raise ValueError(
                    "Individual keyword arguments for key material and the 'jwk' argument are mutually exclusive."
                )
            self._key_material = JsonWebKey(**jwk)
        else:
            self._key_material = JsonWebKey(**kwargs)

    def __repr__(self) -> str:
        return f"<KeyVaultKey [{self.id}]>"[:1024]

    @classmethod
    def _from_key_bundle(cls, key_bundle: "_models.KeyBundle") -> "KeyVaultKey":
        # pylint:disable=protected-access
        return cls(
            key_id=key_bundle.key.kid,  # type: ignore
            jwk={field: getattr(key_bundle.key, field, None) for field in JsonWebKey._FIELDS},
            properties=KeyProperties._from_key_bundle(key_bundle),
        )

    @property
    def id(self) -> str:
        """The key ID.

        :returns: The key ID.
        :rtype: str
        """
        return self._properties.id

    @property
    def name(self) -> str:
        """The key name.

        :returns: The key name.
        :rtype: str
        """
        return self._properties.name

    @property
    def properties(self) -> KeyProperties:
        """The key properties.

        :returns: The key properties.
        :rtype: ~azure.keyvault.keys.KeyProperties
        """
        return self._properties

    @property
    def key(self) -> JsonWebKey:
        """The JSON Web Key (JWK) for the key.

        :returns: The JSON Web Key (JWK) for the key.
        :rtype: ~azure.keyvault.keys.JsonWebKey
        """
        return self._key_material

    @property
    def key_type(self) -> Union[str, KeyType]:
        """The key's type. See :class:`~azure.keyvault.keys.KeyType` for possible values.

        :returns: The key's type. See :class:`~azure.keyvault.keys.KeyType` for possible values.
        :rtype: ~azure.keyvault.keys.KeyType or str
        """
        # pylint:disable=no-member
        return self._key_material.kty  # type: ignore[attr-defined]

    @property
    def key_operations(self) -> List[Union[str, KeyOperation]]:
        """Permitted operations. See :class:`~azure.keyvault.keys.KeyOperation` for possible values.

        :returns: Permitted operations. See :class:`~azure.keyvault.keys.KeyOperation` for possible values.
        :rtype: List[~azure.keyvault.keys.KeyOperation or str]
        """
        # pylint:disable=no-member
        return self._key_material.key_ops  # type: ignore[attr-defined]


class KeyVaultKeyIdentifier(object):
    """Information about a KeyVaultKey parsed from a key ID.

    :param str source_id: The full original identifier of a key

    :raises ValueError: if the key ID is improperly formatted

    Example:
        .. literalinclude:: ../tests/test_parse_id.py
            :start-after: [START parse_key_vault_key_id]
            :end-before: [END parse_key_vault_key_id]
            :language: python
            :caption: Parse a key's ID
            :dedent: 8
    """

    def __init__(self, source_id: str) -> None:
        self._resource_id = parse_key_vault_id(source_id)

    @property
    def source_id(self) -> str:
        return self._resource_id.source_id

    @property
    def vault_url(self) -> str:
        return self._resource_id.vault_url

    @property
    def name(self) -> str:
        return self._resource_id.name

    @property
    def version(self) -> Optional[str]:
        return self._resource_id.version


class DeletedKey(KeyVaultKey):
    """A deleted key's properties, cryptographic material and its deletion information.

    If soft-delete is enabled, returns information about its recovery as well.

    :param properties: Properties of the deleted key.
    :type properties: ~azure.keyvault.keys.KeyProperties
    :param deleted_date: When the key was deleted, in UTC.
    :type deleted_date: ~datetime.datetime or None
    :param recovery_id: An identifier used to recover the deleted key. Returns ``None`` if soft-delete is disabled.
    :type recovery_id: str or None
    :param scheduled_purge_date: When the key is scheduled to be purged, in UTC. Returns ``None`` if soft-delete is
        disabled.
    :type scheduled_purge_date: ~datetime.datetime or None
    """

    def __init__(
        self,
        properties: KeyProperties,
        deleted_date: Optional[datetime] = None,
        recovery_id: Optional[str] = None,
        scheduled_purge_date: Optional[datetime] = None,
        **kwargs: Any,
    ) -> None:
        super(DeletedKey, self).__init__(properties=properties, **kwargs)
        self._deleted_date = deleted_date
        self._recovery_id = recovery_id
        self._scheduled_purge_date = scheduled_purge_date

    def __repr__(self) -> str:
        return f"<DeletedKey [{self.id}]>"[:1024]

    @classmethod
    def _from_deleted_key_bundle(cls, deleted_key_bundle: "_models.DeletedKeyBundle") -> "DeletedKey":
        # pylint:disable=protected-access
        return cls(
            properties=KeyProperties._from_key_bundle(deleted_key_bundle),
            key_id=deleted_key_bundle.key.kid,  # type: ignore
            jwk={field: getattr(deleted_key_bundle.key, field, None) for field in JsonWebKey._FIELDS},
            deleted_date=deleted_key_bundle.deleted_date,
            recovery_id=deleted_key_bundle.recovery_id,
            scheduled_purge_date=deleted_key_bundle.scheduled_purge_date,
        )

    @classmethod
    def _from_deleted_key_item(cls, deleted_key_item: "_models.DeletedKeyItem") -> "DeletedKey":
        return cls(
            properties=KeyProperties._from_key_item(deleted_key_item),  # pylint: disable=protected-access
            key_id=deleted_key_item.kid,
            deleted_date=deleted_key_item.deleted_date,
            recovery_id=deleted_key_item.recovery_id,
            scheduled_purge_date=deleted_key_item.scheduled_purge_date,
        )

    @property
    def deleted_date(self) -> Optional[datetime]:
        """When the key was deleted, in UTC.

        :returns: When the key was deleted, in UTC.
        :rtype: ~datetime.datetime or None
        """
        return self._deleted_date

    @property
    def recovery_id(self) -> Optional[str]:
        """An identifier used to recover the deleted key. Returns ``None`` if soft-delete is disabled.

        :returns: An identifier used to recover the deleted key. Returns ``None`` if soft-delete is disabled.
        :rtype: str or None
        """
        return self._recovery_id

    @property
    def scheduled_purge_date(self) -> Optional[datetime]:
        """When the key is scheduled to be purged, in UTC. Returns ``None`` if soft-delete is disabled.

        :returns: When the key is scheduled to be purged, in UTC. Returns ``None`` if soft-delete is disabled.
        :rtype: ~datetime.datetime or None
        """
        return self._scheduled_purge_date

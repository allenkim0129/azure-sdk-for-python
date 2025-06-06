# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) Python Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


class CertificatePolicyAction(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of the action."""

    EMAIL_CONTACTS = "EmailContacts"
    """A certificate policy that will email certificate contacts."""
    AUTO_RENEW = "AutoRenew"
    """A certificate policy that will auto-renew a certificate."""


class DeletionRecoveryLevel(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Reflects the deletion recovery level currently in effect for secrets in the current vault. If
    it contains 'Purgeable', the secret can be permanently deleted by a privileged user; otherwise,
    only the system can purge the secret, at the end of the retention interval.
    """

    PURGEABLE = "Purgeable"
    """Denotes a vault state in which deletion is an irreversible operation, without the possibility
    for recovery. This level corresponds to no protection being available against a Delete
    operation; the data is irretrievably lost upon accepting a Delete operation at the entity level
    or higher (vault, resource group, subscription etc.)"""
    RECOVERABLE_PURGEABLE = "Recoverable+Purgeable"
    """Denotes a vault state in which deletion is recoverable, and which also permits immediate and
    permanent deletion (i.e. purge). This level guarantees the recoverability of the deleted entity
    during the retention interval (90 days), unless a Purge operation is requested, or the
    subscription is cancelled. System wil permanently delete it after 90 days, if not recovered"""
    RECOVERABLE = "Recoverable"
    """Denotes a vault state in which deletion is recoverable without the possibility for immediate
    and permanent deletion (i.e. purge). This level guarantees the recoverability of the deleted
    entity during the retention interval (90 days) and while the subscription is still available.
    System wil permanently delete it after 90 days, if not recovered"""
    RECOVERABLE_PROTECTED_SUBSCRIPTION = "Recoverable+ProtectedSubscription"
    """Denotes a vault and subscription state in which deletion is recoverable within retention
    interval (90 days), immediate and permanent deletion (i.e. purge) is not permitted, and in
    which the subscription itself  cannot be permanently canceled. System wil permanently delete it
    after 90 days, if not recovered"""
    CUSTOMIZED_RECOVERABLE_PURGEABLE = "CustomizedRecoverable+Purgeable"
    """Denotes a vault state in which deletion is recoverable, and which also permits immediate and
    permanent deletion (i.e. purge when 7 <= SoftDeleteRetentionInDays < 90). This level guarantees
    the recoverability of the deleted entity during the retention interval, unless a Purge
    operation is requested, or the subscription is cancelled."""
    CUSTOMIZED_RECOVERABLE = "CustomizedRecoverable"
    """Denotes a vault state in which deletion is recoverable without the possibility for immediate
    and permanent deletion (i.e. purge when 7 <= SoftDeleteRetentionInDays < 90).This level
    guarantees the recoverability of the deleted entity during the retention interval and while the
    subscription is still available."""
    CUSTOMIZED_RECOVERABLE_PROTECTED_SUBSCRIPTION = "CustomizedRecoverable+ProtectedSubscription"
    """Denotes a vault and subscription state in which deletion is recoverable, immediate and
    permanent deletion (i.e. purge) is not permitted, and in which the subscription itself cannot
    be permanently canceled when 7 <= SoftDeleteRetentionInDays < 90. This level guarantees the
    recoverability of the deleted entity during the retention interval, and also reflects the fact
    that the subscription itself cannot be cancelled."""


class JsonWebKeyCurveName(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Elliptic curve name. For valid values, see JsonWebKeyCurveName."""

    P_256 = "P-256"
    """The NIST P-256 elliptic curve, AKA SECG curve SECP256R1."""
    P_384 = "P-384"
    """The NIST P-384 elliptic curve, AKA SECG curve SECP384R1."""
    P_521 = "P-521"
    """The NIST P-521 elliptic curve, AKA SECG curve SECP521R1."""
    P_256K = "P-256K"
    """The SECG SECP256K1 elliptic curve."""


class JsonWebKeyType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The type of key pair to be used for the certificate."""

    EC = "EC"
    """Elliptic Curve."""
    EC_HSM = "EC-HSM"
    """Elliptic Curve with a private key which is not exportable from the HSM."""
    RSA = "RSA"
    """RSA (`https://tools.ietf.org/html/rfc3447 <https://tools.ietf.org/html/rfc3447>`_)."""
    RSA_HSM = "RSA-HSM"
    """RSA with a private key which is not exportable from the HSM."""
    OCT = "oct"
    """Octet sequence (used to represent symmetric keys)."""
    OCT_HSM = "oct-HSM"
    """Octet sequence with a private key which is not exportable from the HSM."""


class KeyUsageType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Supported usages of a certificate key."""

    DIGITAL_SIGNATURE = "digitalSignature"
    """Indicates that the certificate key can be used as a digital signature."""
    NON_REPUDIATION = "nonRepudiation"
    """Indicates that the certificate key can be used for authentication."""
    KEY_ENCIPHERMENT = "keyEncipherment"
    """Indicates that the certificate key can be used for key encryption."""
    DATA_ENCIPHERMENT = "dataEncipherment"
    """Indicates that the certificate key can be used for data encryption."""
    KEY_AGREEMENT = "keyAgreement"
    """Indicates that the certificate key can be used to determine key agreement, such as a key
    created using the Diffie-Hellman key agreement algorithm."""
    KEY_CERT_SIGN = "keyCertSign"
    """Indicates that the certificate key can be used to sign certificates."""
    C_RL_SIGN = "cRLSign"
    """Indicates that the certificate key can be used to sign a certificate revocation list."""
    ENCIPHER_ONLY = "encipherOnly"
    """Indicates that the certificate key can be used for encryption only."""
    DECIPHER_ONLY = "decipherOnly"
    """Indicates that the certificate key can be used for decryption only."""

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
# pylint: disable=docstring-keyword-should-match-keyword-only

from typing import (
    Any, Callable, cast, Optional, Union,
    TYPE_CHECKING
)
from urllib.parse import parse_qs

from azure.storage.blob import generate_account_sas as generate_blob_account_sas
from azure.storage.blob import generate_blob_sas, generate_container_sas
from ._shared.models import Services
from ._shared.shared_access_signature import QueryStringConstants


if TYPE_CHECKING:
    from azure.storage.blob import BlobSasPermissions, ContainerSasPermissions
    from azure.storage.blob._shared.models import Services as BlobServices
    from datetime import datetime
    from ._models import (
        AccountSasPermissions,
        DirectorySasPermissions,
        FileSasPermissions,
        FileSystemSasPermissions,
        ResourceTypes,
        UserDelegationKey
    )


def generate_account_sas(
    account_name: str,
    account_key: str,
    resource_types: Union["ResourceTypes", str],
    permission: Union["AccountSasPermissions", str],
    expiry: Union["datetime", str],
    *,
    services: Union[Services, str] = Services(blob=True),
    sts_hook: Optional[Callable[[str], None]] = None,
    **kwargs: Any
) -> str:
    """Generates a shared access signature for the DataLake service.

    Use the returned signature as the credential parameter of any DataLakeServiceClient,
    FileSystemClient, DataLakeDirectoryClient or DataLakeFileClient.

    :param str account_name:
        The storage account name used to generate the shared access signature.
    :param str account_key:
        The access key to generate the shared access signature.
    :param resource_types:
        Specifies the resource types that are accessible with the account SAS.
    :type resource_types: str or ~azure.storage.filedatalake.ResourceTypes
    :param permission:
        The permissions associated with the shared access signature. The
        user is restricted to operations allowed by the permissions.
    :type permission: str or ~azure.storage.filedatalake.AccountSasPermissions
    :param expiry:
        The time at which the shared access signature becomes invalid.
        The provided datetime will always be interpreted as UTC.
    :type expiry: ~datetime.datetime or str
    :keyword start:
        The time at which the shared access signature becomes valid. If
        omitted, start time for this call is assumed to be the time when the
        storage service receives the request. The provided datetime will always
        be interpreted as UTC.
    :paramtype start: ~datetime.datetime or str
    :keyword str ip:
        Specifies an IP address or a range of IP addresses from which to accept requests.
        If the IP address from which the request originates does not match the IP address
        or address range specified on the SAS token, the request is not authenticated.
        For example, specifying ip=168.1.5.65 or ip=168.1.5.60-168.1.5.70 on the SAS
        restricts the request to those IP addresses.
    :keyword Union[Services, str] services:
        Specifies the services that the Shared Access Signature (sas) token will be able to be utilized with.
        Will default to only this package (i.e. blobs) if not provided.
    :paramtype services: Services or str
    :keyword str protocol:
        Specifies the protocol permitted for a request made. The default value is https.
    :keyword str encryption_scope:
        Specifies the encryption scope for a request made so that all write operations will be service encrypted.
    :keyword sts_hook:
        For debugging purposes only. If provided, the hook is called with the string to sign
        that was used to generate the SAS.
    :paramtype sts_hook: ~typing.Callable[[str], None] or None
    :return: A Shared Access Signature (sas) token.
    :rtype: str
    """
    return generate_blob_account_sas(
        account_name=account_name,
        account_key=account_key,
        resource_types=resource_types,
        permission=permission,
        expiry=expiry,
        services=cast(Union["BlobServices", str], services),
        sts_hook=sts_hook,
        **kwargs
    )


def generate_file_system_sas(
    account_name: str,
    file_system_name: str,
    credential: Union[str, "UserDelegationKey"],
    permission: Optional[Union["FileSystemSasPermissions", str]] = None,
    expiry: Optional[Union["datetime", str]] = None,
    *,
    sts_hook: Optional[Callable[[str], None]] = None,
    **kwargs: Any
) -> str:
    """Generates a shared access signature for a file system.

    Use the returned signature with the credential parameter of any DataLakeServiceClient,
    FileSystemClient, DataLakeDirectoryClient or DataLakeFileClient.

    :param str account_name:
        The storage account name used to generate the shared access signature.
    :param str file_system_name:
        The name of the file system.
    :param credential:
        Credential could be either account key or user delegation key.
        If use account key is used as credential, then the credential type should be a str.
        Instead of an account key, the user could also pass in a user delegation key.
        A user delegation key can be obtained from the service by authenticating with an AAD identity;
        this can be accomplished
        by calling :func:`~azure.storage.filedatalake.DataLakeServiceClient.get_user_delegation_key`.
        When present, the SAS is signed with the user delegation key instead.
    :type credential: str or ~azure.storage.filedatalake.UserDelegationKey
    :param permission:
        The permissions associated with the shared access signature. The
        user is restricted to operations allowed by the permissions.
        Permissions must be ordered racwdlmeop.
        Required unless an id is given referencing a stored access policy
        which contains this field. This field must be omitted if it has been
        specified in an associated stored access policy.
    :type permission: str or ~azure.storage.filedatalake.FileSystemSasPermissions or None
    :param expiry:
        The time at which the shared access signature becomes invalid.
        Required unless an id is given referencing a stored access policy
        which contains this field. This field must be omitted if it has
        been specified in an associated stored access policy. Azure will always
        convert values to UTC. If a date is passed in without timezone info, it
        is assumed to be UTC.
    :type expiry: datetime or str or None
    :keyword start:
        The time at which the shared access signature becomes valid. If
        omitted, start time for this call is assumed to be the time when the
        storage service receives the request. The provided datetime will always
        be interpreted as UTC.
    :paramtype start: datetime or str
    :keyword str policy_id:
        A unique value up to 64 characters in length that correlates to a
        stored access policy. To create a stored access policy, use
        :func:`~azure.storage.filedatalake.FileSystemClient.set_file_system_access_policy`.
    :keyword str ip:
        Specifies an IP address or a range of IP addresses from which to accept requests.
        If the IP address from which the request originates does not match the IP address
        or address range specified on the SAS token, the request is not authenticated.
        For example, specifying ip=168.1.5.65 or ip=168.1.5.60-168.1.5.70 on the SAS
        restricts the request to those IP addresses.
    :keyword str protocol:
        Specifies the protocol permitted for a request made. The default value is https.
    :keyword str cache_control:
        Response header value for Cache-Control when resource is accessed
        using this shared access signature.
    :keyword str content_disposition:
        Response header value for Content-Disposition when resource is accessed
        using this shared access signature.
    :keyword str content_encoding:
        Response header value for Content-Encoding when resource is accessed
        using this shared access signature.
    :keyword str content_language:
        Response header value for Content-Language when resource is accessed
        using this shared access signature.
    :keyword str content_type:
        Response header value for Content-Type when resource is accessed
        using this shared access signature.
    :keyword str preauthorized_agent_object_id:
        The AAD object ID of a user assumed to be authorized by the owner of the user delegation key to perform
        the action granted by the SAS token. The service will validate the SAS token and ensure that the owner of the
        user delegation key has the required permissions before granting access but no additional permission check for
        the agent object id will be performed.
    :keyword str agent_object_id:
        The AAD object ID of a user assumed to be unauthorized by the owner of the user delegation key to
        perform the action granted by the SAS token. The service will validate the SAS token and ensure that the owner
        of the user delegation key has the required permissions before granting access and the service will perform an
        additional POSIX ACL check to determine if this user is authorized to perform the requested operation.
    :keyword str correlation_id:
        The correlation id to correlate the storage audit logs with the audit logs used by the principal
        generating and distributing the SAS.
    :keyword str encryption_scope:
        Specifies the encryption scope for a request made so that all write operations will be service encrypted.
    :keyword sts_hook:
        For debugging purposes only. If provided, the hook is called with the string to sign
        that was used to generate the SAS.
    :paramtype sts_hook: ~typing.Callable[[str], None] or None
    :return: A Shared Access Signature (sas) token.
    :rtype: str
    """
    return generate_container_sas(
        account_name=account_name,
        container_name=file_system_name,
        account_key=credential if isinstance(credential, str) else None,
        user_delegation_key=credential if not isinstance(credential, str) else None,
        permission=cast(Optional[Union["ContainerSasPermissions", str]], permission),
        expiry=expiry,
        sts_hook=sts_hook,
        **kwargs
    )


def generate_directory_sas(
    account_name: str,
    file_system_name: str,
    directory_name: str,
    credential: Union[str, "UserDelegationKey"],
    permission: Optional[Union["DirectorySasPermissions", str]] = None,
    expiry: Optional[Union["datetime", str]] = None,
    *,
    sts_hook: Optional[Callable[[str], None]] = None,
    **kwargs: Any
) -> str:
    """Generates a shared access signature for a directory.

    Use the returned signature with the credential parameter of any DataLakeServiceClient,
    FileSystemClient, DataLakeDirectoryClient or DataLakeFileClient.

    :param str account_name:
        The storage account name used to generate the shared access signature.
    :param str file_system_name:
        The name of the file system.
    :param str directory_name:
        The name of the directory.
    :param str credential:
        Credential could be either account key or user delegation key.
        If use account key is used as credential, then the credential type should be a str.
        Instead of an account key, the user could also pass in a user delegation key.
        A user delegation key can be obtained from the service by authenticating with an AAD identity;
        this can be accomplished
        by calling :func:`~azure.storage.filedatalake.DataLakeServiceClient.get_user_delegation_key`.
        When present, the SAS is signed with the user delegation key instead.
    :type credential: str or ~azure.storage.filedatalake.UserDelegationKey
    :param permission:
        The permissions associated with the shared access signature. The
        user is restricted to operations allowed by the permissions.
        Permissions must be ordered racwdlmeop.
        Required unless an id is given referencing a stored access policy
        which contains this field. This field must be omitted if it has been
        specified in an associated stored access policy.
    :type permission: str or ~azure.storage.filedatalake.DirectorySasPermissions or None
    :param expiry:
        The time at which the shared access signature becomes invalid.
        Required unless an id is given referencing a stored access policy
        which contains this field. This field must be omitted if it has
        been specified in an associated stored access policy. Azure will always
        convert values to UTC. If a date is passed in without timezone info, it
        is assumed to be UTC.
    :type expiry: ~datetime.datetime or str or None
    :keyword start:
        The time at which the shared access signature becomes valid. If
        omitted, start time for this call is assumed to be the time when the
        storage service receives the request. The provided datetime will always
        be interpreted as UTC.
    :paramtype start: ~datetime.datetime or str
    :keyword str policy_id:
        A unique value up to 64 characters in length that correlates to a
        stored access policy. To create a stored access policy, use
        :func:`~azure.storage.filedatalake.FileSystemClient.set_file_system_access_policy`.
    :keyword str ip:
        Specifies an IP address or a range of IP addresses from which to accept requests.
        If the IP address from which the request originates does not match the IP address
        or address range specified on the SAS token, the request is not authenticated.
        For example, specifying ip=168.1.5.65 or ip=168.1.5.60-168.1.5.70 on the SAS
        restricts the request to those IP addresses.
    :keyword str protocol:
        Specifies the protocol permitted for a request made. The default value is https.
    :keyword str cache_control:
        Response header value for Cache-Control when resource is accessed
        using this shared access signature.
    :keyword str content_disposition:
        Response header value for Content-Disposition when resource is accessed
        using this shared access signature.
    :keyword str content_encoding:
        Response header value for Content-Encoding when resource is accessed
        using this shared access signature.
    :keyword str content_language:
        Response header value for Content-Language when resource is accessed
        using this shared access signature.
    :keyword str content_type:
        Response header value for Content-Type when resource is accessed
        using this shared access signature.
    :keyword str preauthorized_agent_object_id:
        The AAD object ID of a user assumed to be authorized by the owner of the user delegation key to perform
        the action granted by the SAS token. The service will validate the SAS token and ensure that the owner of the
        user delegation key has the required permissions before granting access but no additional permission check for
        the agent object id will be performed.
    :keyword str agent_object_id:
        The AAD object ID of a user assumed to be unauthorized by the owner of the user delegation key to
        perform the action granted by the SAS token. The service will validate the SAS token and ensure that the owner
        of the user delegation key has the required permissions before granting access and the service will perform an
        additional POSIX ACL check to determine if this user is authorized to perform the requested operation.
    :keyword str correlation_id:
        The correlation id to correlate the storage audit logs with the audit logs used by the principal
        generating and distributing the SAS.
    :keyword str encryption_scope:
        Specifies the encryption scope for a request made so that all write operations will be service encrypted.
    :keyword sts_hook:
        For debugging purposes only. If provided, the hook is called with the string to sign
        that was used to generate the SAS.
    :paramtype sts_hook: ~typing.Callable[[str], None] or None
    :return: A Shared Access Signature (sas) token.
    :rtype: str
    """
    depth = len(directory_name.strip("/").split("/"))
    return generate_blob_sas(
        account_name=account_name,
        container_name=file_system_name,
        blob_name=directory_name,
        account_key=credential if isinstance(credential, str) else None,
        user_delegation_key=credential if not isinstance(credential, str) else None,
        permission=cast(Optional[Union["BlobSasPermissions", str]], permission),
        expiry=expiry,
        sdd=depth,
        is_directory=True,
        sts_hook=sts_hook,
        **kwargs
    )


def generate_file_sas(
    account_name: str,
    file_system_name: str,
    directory_name: str,
    file_name: str,
    credential: Union[str, "UserDelegationKey"],
    permission: Optional[Union["FileSasPermissions", str]] = None,
    expiry: Optional[Union["datetime", str]] = None,
    *,
    sts_hook: Optional[Callable[[str], None]] = None,
    **kwargs: Any
) -> str:
    """Generates a shared access signature for a file.

    Use the returned signature with the credential parameter of any BDataLakeServiceClient,
    FileSystemClient, DataLakeDirectoryClient or DataLakeFileClient.

    :param str account_name:
        The storage account name used to generate the shared access signature.
    :param str file_system_name:
        The name of the file system.
    :param str directory_name:
        The name of the directory.
    :param str file_name:
        The name of the file.
    :param str credential:
        Credential could be either account key or user delegation key.
        If use account key is used as credential, then the credential type should be a str.
        Instead of an account key, the user could also pass in a user delegation key.
        A user delegation key can be obtained from the service by authenticating with an AAD identity;
        this can be accomplished
        by calling :func:`~azure.storage.filedatalake.DataLakeServiceClient.get_user_delegation_key`.
        When present, the SAS is signed with the user delegation key instead.
    :type credential: str or ~azure.storage.filedatalake.UserDelegationKey
    :param permission:
        The permissions associated with the shared access signature. The
        user is restricted to operations allowed by the permissions.
        Permissions must be ordered racwdlmeop.
        Required unless an id is given referencing a stored access policy
        which contains this field. This field must be omitted if it has been
        specified in an associated stored access policy.
    :type permission: str or ~azure.storage.filedatalake.FileSasPermissions or None
    :param expiry:
        The time at which the shared access signature becomes invalid.
        Required unless an id is given referencing a stored access policy
        which contains this field. This field must be omitted if it has
        been specified in an associated stored access policy. Azure will always
        convert values to UTC. If a date is passed in without timezone info, it
        is assumed to be UTC.
    :type expiry: ~datetime.datetime or str or None
    :keyword start:
        The time at which the shared access signature becomes valid. If
        omitted, start time for this call is assumed to be the time when the
        storage service receives the request. The provided datetime will always
        be interpreted as UTC.
    :paramtype start: ~datetime.datetime or str
    :keyword str policy_id:
        A unique value up to 64 characters in length that correlates to a
        stored access policy. To create a stored access policy, use
        :func:`~azure.storage.filedatalake.FileSystemClient.set_file_system_access_policy`.
    :keyword str ip:
        Specifies an IP address or a range of IP addresses from which to accept requests.
        If the IP address from which the request originates does not match the IP address
        or address range specified on the SAS token, the request is not authenticated.
        For example, specifying ip=168.1.5.65 or ip=168.1.5.60-168.1.5.70 on the SAS
        restricts the request to those IP addresses.
    :keyword str protocol:
        Specifies the protocol permitted for a request made. The default value is https.
    :keyword str cache_control:
        Response header value for Cache-Control when resource is accessed
        using this shared access signature.
    :keyword str content_disposition:
        Response header value for Content-Disposition when resource is accessed
        using this shared access signature.
    :keyword str content_encoding:
        Response header value for Content-Encoding when resource is accessed
        using this shared access signature.
    :keyword str content_language:
        Response header value for Content-Language when resource is accessed
        using this shared access signature.
    :keyword str content_type:
        Response header value for Content-Type when resource is accessed
        using this shared access signature.
    :keyword str preauthorized_agent_object_id:
        The AAD object ID of a user assumed to be authorized by the owner of the user delegation key to perform
        the action granted by the SAS token. The service will validate the SAS token and ensure that the owner of the
        user delegation key has the required permissions before granting access but no additional permission check for
        the agent object id will be performed.
    :keyword str agent_object_id:
        The AAD object ID of a user assumed to be unauthorized by the owner of the user delegation key to
        perform the action granted by the SAS token. The service will validate the SAS token and ensure that the owner
        of the user delegation key has the required permissions before granting access and the service will perform an
        additional POSIX ACL check to determine if this user is authorized to perform the requested operation.
    :keyword str correlation_id:
        The correlation id to correlate the storage audit logs with the audit logs used by the principal
        generating and distributing the SAS. This can only be used when generating a SAS with delegation key.
    :keyword str encryption_scope:
        Specifies the encryption scope for a request made so that all write operations will be service encrypted.
    :keyword sts_hook:
        For debugging purposes only. If provided, the hook is called with the string to sign
        that was used to generate the SAS.
    :paramtype sts_hook: ~typing.Callable[[str], None] or None
    :return: A Shared Access Signature (sas) token.
    :rtype: str
    """
    if directory_name:
        path = directory_name.rstrip('/') + "/" + file_name
    else:
        path = file_name
    return generate_blob_sas(
        account_name=account_name,
        container_name=file_system_name,
        blob_name=path,
        account_key=credential if isinstance(credential, str) else None,
        user_delegation_key=credential if not isinstance(credential, str) else None,
        permission=cast(Optional[Union["BlobSasPermissions", str]], permission),
        expiry=expiry,
        sts_hook=sts_hook,
        **kwargs
    )

def _is_credential_sastoken(credential: Any) -> bool:
    if not credential or not isinstance(credential, str):
        return False

    sas_values = QueryStringConstants.to_list()
    parsed_query = parse_qs(credential.lstrip("?"))
    if parsed_query and all(k in sas_values for k in parsed_query):
        return True
    return False

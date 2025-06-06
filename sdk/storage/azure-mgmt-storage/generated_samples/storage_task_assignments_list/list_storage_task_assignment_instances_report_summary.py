# pylint: disable=line-too-long,useless-suppression
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from azure.identity import DefaultAzureCredential

from azure.mgmt.storage import StorageManagementClient

"""
# PREREQUISITES
    pip install azure-identity
    pip install azure-mgmt-storage
# USAGE
    python list_storage_task_assignment_instances_report_summary.py

    Before run the sample, please set the values of the client ID, tenant ID and client secret
    of the AAD application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET. For more info about how to get the value, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""


def main():
    client = StorageManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="1f31ba14-ce16-4281-b9b4-3e78da6e1616",
    )

    response = client.storage_task_assignment_instances_report.list(
        resource_group_name="res4228",
        account_name="sto4445",
        storage_task_assignment_name="myassignment1",
    )
    for item in response:
        print(item)


# x-ms-original-file: specification/storage/resource-manager/Microsoft.Storage/stable/2024-01-01/examples/storageTaskAssignmentsList/ListStorageTaskAssignmentInstancesReportSummary.json
if __name__ == "__main__":
    main()

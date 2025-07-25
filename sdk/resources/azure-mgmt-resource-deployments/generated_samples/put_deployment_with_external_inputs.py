# pylint: disable=line-too-long,useless-suppression
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from azure.identity import DefaultAzureCredential

from azure.mgmt.resource.deployments import DeploymentsMgmtClient

"""
# PREREQUISITES
    pip install azure-identity
    pip install azure-mgmt-resource-deployments
# USAGE
    python put_deployment_with_external_inputs.py

    Before run the sample, please set the values of the client ID, tenant ID and client secret
    of the AAD application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET. For more info about how to get the value, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""


def main():
    client = DeploymentsMgmtClient(
        credential=DefaultAzureCredential(),
        subscription_id="00000000-0000-0000-0000-000000000001",
    )

    response = client.deployments.begin_create_or_update(
        resource_group_name="my-resource-group",
        deployment_name="my-deployment",
        parameters={
            "properties": {
                "externalInputDefinitions": {"fooValue": {"config": "FOO_VALUE", "kind": "sys.envVar"}},
                "externalInputs": {"fooValue": {"value": "baz"}},
                "mode": "Incremental",
                "parameters": {"inputObj": {"expression": "[createObject('foo', externalInputs('fooValue'))]"}},
                "template": {
                    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
                    "contentVersion": "1.0.0.0",
                    "outputs": {"inputObj": {"type": "object", "value": "[parameters('inputObj')]"}},
                    "parameters": {"inputObj": {"type": "object"}},
                    "resources": [],
                },
            }
        },
    ).result()
    print(response)


# x-ms-original-file: specification/resources/resource-manager/Microsoft.Resources/deployments/stable/2025-04-01/examples/PutDeploymentWithExternalInputs.json
if __name__ == "__main__":
    main()

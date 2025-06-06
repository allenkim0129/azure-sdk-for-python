# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.network.aio import NetworkManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer
from devtools_testutils.aio import recorded_by_proxy_async

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestNetworkManagementExpressRouteCrossConnectionPeeringsOperationsAsync(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(NetworkManagementClient, is_async=True)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_express_route_cross_connection_peerings_list(self, resource_group):
        response = self.client.express_route_cross_connection_peerings.list(
            resource_group_name=resource_group.name,
            cross_connection_name="str",
            api_version="2024-07-01",
        )
        result = [r async for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_express_route_cross_connection_peerings_begin_delete(self, resource_group):
        response = await (
            await self.client.express_route_cross_connection_peerings.begin_delete(
                resource_group_name=resource_group.name,
                cross_connection_name="str",
                peering_name="str",
                api_version="2024-07-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_express_route_cross_connection_peerings_get(self, resource_group):
        response = await self.client.express_route_cross_connection_peerings.get(
            resource_group_name=resource_group.name,
            cross_connection_name="str",
            peering_name="str",
            api_version="2024-07-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_express_route_cross_connection_peerings_begin_create_or_update(self, resource_group):
        response = await (
            await self.client.express_route_cross_connection_peerings.begin_create_or_update(
                resource_group_name=resource_group.name,
                cross_connection_name="str",
                peering_name="str",
                peering_parameters={
                    "azureASN": 0,
                    "etag": "str",
                    "gatewayManagerEtag": "str",
                    "id": "str",
                    "ipv6PeeringConfig": {
                        "microsoftPeeringConfig": {
                            "advertisedCommunities": ["str"],
                            "advertisedPublicPrefixInfo": [
                                {"prefix": "str", "signature": "str", "validationId": "str", "validationState": "str"}
                            ],
                            "advertisedPublicPrefixes": ["str"],
                            "advertisedPublicPrefixesState": "str",
                            "customerASN": 0,
                            "legacyMode": 0,
                            "routingRegistryName": "str",
                        },
                        "primaryPeerAddressPrefix": "str",
                        "routeFilter": {"id": "str"},
                        "secondaryPeerAddressPrefix": "str",
                        "state": "str",
                    },
                    "lastModifiedBy": "str",
                    "microsoftPeeringConfig": {
                        "advertisedCommunities": ["str"],
                        "advertisedPublicPrefixInfo": [
                            {"prefix": "str", "signature": "str", "validationId": "str", "validationState": "str"}
                        ],
                        "advertisedPublicPrefixes": ["str"],
                        "advertisedPublicPrefixesState": "str",
                        "customerASN": 0,
                        "legacyMode": 0,
                        "routingRegistryName": "str",
                    },
                    "name": "str",
                    "peerASN": 0,
                    "peeringType": "str",
                    "primaryAzurePort": "str",
                    "primaryPeerAddressPrefix": "str",
                    "provisioningState": "str",
                    "secondaryAzurePort": "str",
                    "secondaryPeerAddressPrefix": "str",
                    "sharedKey": "str",
                    "state": "str",
                    "vlanId": 0,
                },
                api_version="2024-07-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

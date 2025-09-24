# The MIT License (MIT)
# Copyright (c) Microsoft Corporation. All rights reserved.

import random
import unittest
import uuid
from typing import List

import pytest

import azure.cosmos.aio._retry_utility_async as retry_utility
import azure.cosmos.exceptions as exceptions
import test_config
from azure.cosmos import http_constants, _endpoint_discovery_retry_policy
from azure.cosmos._execution_context.query_execution_info import _PartitionedQueryExecutionInfo
from azure.cosmos._retry_options import RetryOptions
from azure.cosmos.aio import CosmosClient, DatabaseProxy, ContainerProxy
from azure.cosmos.documents import _DistinctType
from azure.cosmos.partition_key import PartitionKey

PARTITION_KEY = 'pk'

async def run_queries(container, iterations):
    ret_list = []
    for i in range(iterations):
        curr = str(random.randint(0, 10))
        query = 'SELECT * FROM c WHERE c.attr1=' + curr + ' order by c.attr1'
        qlist = [item async for item in container.query_items(query=query)]
        ret_list.append((curr, qlist))
    for ret in ret_list:
        curr = ret[0]
        if len(ret[1]) != 0:
            for results in ret[1]:
                attr_number = results['attr1']
                assert str(attr_number) == curr  # verify that all results match their randomly generated attributes
        print("validation succeeded for all query results")

def create_body(partition_key_value):
    body = {
        'id': 'Item_' + str(uuid.uuid4()),
        PARTITION_KEY: partition_key_value,
        'attr1': random.randint(0, 10),
    }
    return body

async def create_items(container, num_items=100, pk_values=(19, 0, 1, 6, 7)) -> List[ContainerProxy]:
    items = []
    for i in range(num_items):
        body = create_body(pk_values[i % len(pk_values)])
        item = await container.create_item(body=body)
        items.append(item)
    return items

async def check_distribution(container):
    feed_ranges = [item async for item in container.read_feed_ranges()]
    num_items = 0
    i = 0
    for feed_range in feed_ranges:
        query = "SELECT * FROM c"
        items = [item async for item in container.query_items(query=query, feed_range=feed_range)]
        if len(items) == 0:
            print(f'partition {i} - num_items: {len(items)}')
        else:
            print(f'partition {i} - num_items: {len(items)}, a pk value: {items[0]["pk"]}')
        num_items += len(items)
        i += 1

async def delete_all_items(container):
    all_items = [item async for item in container.read_all_items()]
    for item in all_items:
        await container.delete_item(item=item, partition_key=item[PARTITION_KEY])
    print("All items deleted.")

@pytest.mark.cosmosCircuitBreaker
@pytest.mark.cosmosQuery
class TestPartitionMergeQueryAsync(unittest.IsolatedAsyncioTestCase):
    """Test to ensure escaping of non-ascii characters from partition key"""

    created_db: DatabaseProxy = None
    created_container: ContainerProxy = None
    client: CosmosClient = None
    config = test_config.TestConfig
    host = config.host
    masterKey = config.masterKey
    connectionPolicy = config.connectionPolicy
    throughput = config.THROUGHPUT_FOR_5_PARTITIONS
    throughput_after_merge = config.THROUGHPUT_FOR_1_PARTITION
    TEST_DATABASE_ID = "Multi-partition-db"
    TEST_CONTAINER_ID = "Multi-partition-col"


    @classmethod
    def setUpClass(cls):
        pass

    async def asyncSetUp(self):
        self.client = CosmosClient(self.host, self.masterKey)
        self.created_db = await self.client.create_database_if_not_exists(self.TEST_DATABASE_ID)
        self.partition_key = PartitionKey(path="/pk")
        self.container = await self.created_db.create_container_if_not_exists(
            id=self.TEST_CONTAINER_ID,
            partition_key=self.partition_key,
            offer_throughput=self.throughput
        )

        # # case 2: items existed in each partition
        # target_num_items = 10  # more items?
        # self.created_item = await create_items(self.container, target_num_items, [19, 0, 1, 6, 7])
        # await check_distribution(self.container)

        # # case 3: some items existed in some partitions, but not all partitions
        # target_num_items = 10  # more items?
        # self.created_item = await create_items(self.container, target_num_items, [19, 19, 0, 1, 1])
        # await check_distribution(self.container)

        target_throughput = self.config.THROUGHPUT_FOR_1_PARTITION
        await self.container.replace_throughput(target_throughput)

    async def test_read(self):
        properties = await self.container.read()
        assert properties['id'] == self.TEST_CONTAINER_ID
        assert properties['partitionKey'] == self.partition_key


    async def test_read_item(self):
        created_items = await create_items(self.container, 10)
        attributes = ['id', PARTITION_KEY, 'attr1']
        for expected_item in created_items:
            actual_item = await self.container.read_item(item=expected_item, partition_key=expected_item[PARTITION_KEY])
            for attr in attributes:
                assert attr in actual_item, f"Attribute {attr} not found in the item."
                assert actual_item[attr] == expected_item[attr], f"Expected {expected_item[attr]} for {attr}, but got {actual_item[attr]}."

    async def test_read_all_items(self):
        # read_all_items: first read all and delete all items
        await delete_all_items(self.container)

        # read all items again to check if all items were deleted
        all_items_after_delete = [item async for item in self.container.read_all_items()]
        assert len(all_items_after_delete) == 0, "All items should be deleted, but found some items."

        # create items again
        created_items = await create_items(self.container, 10)

        # read all items
        all_items = [item async for item in self.container.read_all_items()]
        assert len(all_items) == len(created_items), "Number of items read does not match the number of created items."

    # add test to certain partiton
    async def test_query_items_change_feed(self):
        # store continuation token
        query_iterable = self.container.query_items_change_feed(
            is_start_from_beginning=True,
        )
        change_feeds = [item async for item in query_iterable]
        continuation1 = self.container.client_connection.last_response_headers['etag']

        # create some items
        num_created_items = 10
        await create_items(self.container, num_created_items)

        query_iterable = self.container.query_items_change_feed(
            continuation=continuation1
        )
        change_feeds = [item async for item in query_iterable]
        assert num_created_items == len(change_feeds)

    # add test to certain partition
    async def test_query_items(self):
        # create items
        target_num_items = 10
        await create_items(self.container, target_num_items, [19, 0, 1, 6, 7])

        # run queries
        await run_queries(self.container, 10)

    async def test_replace_item(self):
        # create items
        target_num_items = 10
        created_items = await create_items(self.container, target_num_items)

        # replace items
        for item in created_items:
            new_item_body = {
                'id': item['id'],
                'pk': item[PARTITION_KEY],
                'attr1': item['attr1'],
                'new_attr': 'new_value'
            }
            updated_item = await self.container.replace_item(item=item, body=new_item_body)
            assert updated_item['new_attr'] == new_item_body['new_attr']

    async def test_upsert_item(self):
        # create items
        target_num_items = 10
        created_items = await create_items(self.container, target_num_items)

        # upsert items
        for item in created_items:
            new_item_body = {
                'id': item['id'],
                'pk': item[PARTITION_KEY],
                'attr1': item['attr1'],
                'new_attr': 'new_value'
            }
            upserted_item = await self.container.upsert_item(body=new_item_body)
            assert upserted_item['new_attr'] == new_item_body['new_attr']

    async def test_create_item(self):
        # create items
        target_num_items = 10
        created_items = await create_items(self.container, target_num_items)

        # verify created items
        for item in created_items:
            actual_item = await self.container.read_item(item=item['id'], partition_key=item['pk'])
            assert actual_item['id'] == item['id']
            assert actual_item['pk'] == item[PARTITION_KEY]
            assert actual_item['attr1'] == item['attr1']

    async def test_patch_item(self):
        # read_all_items: first read all and delete all items, and run read all to check if all items were deleted
        await delete_all_items(self.container)

        items = await create_items(self.container, 10)

        operations = [
            {"op": "add", "path": "/attr1", "value": f'Data-{str(uuid.uuid4())}'},
        ]
        for item in items:
            await self.container.patch_item(item=item, partition_key=item['pk'],
                                 patch_operations=operations)

    async def test_execute_item_batch(self):
        await delete_all_items(self.container)

        num_items = 10
        partition_key_value = 1
        batch_operations = []
        for i in range(num_items):
            body = create_body(partition_key_value)
            batch_operations.append(("create", (
                body,
            )))

        await self.container.execute_item_batch(batch_operations=batch_operations, partition_key=partition_key_value)

        # Verify that all items were created
        for operation in batch_operations:
            body = operation[1][0]
            item = await self.container.read_item(item=body['id'], partition_key=body['pk'])
            assert item['id'] == body['id']
            assert item['pk'] == body['pk']

    # test replacing throughput and get throughput
    async def test_replace_throughput(self):
        # store original throughput
        original_throughput = await self.container.get_throughput()
        print("Original throughput: {}".format(original_throughput.offer_throughput))
        # Replace throughput to merge partitions
        target_throughput = 500
        await self.container.replace_throughput(target_throughput)

        # Verify that the throughput was replaced
        throughput = await self.container.get_throughput()
        print("Replaced throughput: {}".format(throughput.offer_throughput))
        assert throughput.offer_throughput == target_throughput

        # revert to original throughput
        await self.container.replace_throughput(original_throughput.offer_throughput)

    async def test_read_feed_ranges(self):
        feed_ranges = [item async for item in self.container.read_feed_ranges()]
        print("Number of feed ranges: {}".format(len(feed_ranges)))

        target_num_feed_ranges = 1 # expect 1 feed range after merge
        assert target_num_feed_ranges == len(feed_ranges)

if __name__ == '__main__':
    unittest.main()

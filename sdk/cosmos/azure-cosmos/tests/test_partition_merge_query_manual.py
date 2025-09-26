# The MIT License (MIT)
# Copyright (c) Microsoft Corporation. All rights reserved.

import random
import time
import unittest
import uuid
import os

import pytest

import azure.cosmos.cosmos_client as cosmos_client
import test_config
from azure.cosmos import DatabaseProxy, PartitionKey, ContainerProxy
from azure.cosmos.exceptions import CosmosResourceNotFoundError, CosmosHttpResponseError
from typing import List
from azure.cosmos import http_constants
from azure.cosmos import _base as base

PARTITION_KEY = 'pk'
DEFAULT_NUMBER_OF_ITEMS = 100
DEFAULT_PARTITION_KEY_VALUES = (19, 0, 1, 6, 7)
def get_test_item():
    test_item = {
        'id': 'Item_' + str(uuid.uuid4()),
        'test_object': True,
        'lastName': 'Smith',
        'attr1': random.randint(0, 10)
    }
    return test_item


def run_queries(container, iterations):
    ret_list = []
    for i in range(iterations):
        curr = str(random.randint(0, 10))
        query = 'SELECT * FROM c WHERE c.attr1=' + curr + ' order by c.attr1'
        qlist = list(container.query_items(query=query, enable_cross_partition_query=True))
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

def create_items(container, num_items=DEFAULT_NUMBER_OF_ITEMS, pk_values=DEFAULT_PARTITION_KEY_VALUES) -> List[ContainerProxy]:
    items = []
    for i in range(num_items):
        body = create_body(pk_values[i % len(pk_values)])
        item = container.create_item(body=body)
        items.append(item)
    return items

def check_distribution(container):
    feed_ranges = list(container.read_feed_ranges())
    num_items = 0
    i = 0
    for feed_range in feed_ranges:
        query = "SELECT * FROM c"
        items = list(container.query_items(query=query, feed_range=feed_range))
        if len(items) == 0:
            continue
        print(f'partition {i} - num_items: {len(items)}, a pk value: {items[0]["pk"]}')
        num_items += len(items)
        i += 1

def delete_all_items(container):
    all_items = list(container.read_all_items())
    for item in all_items:
        container.delete_item(item=item, partition_key=item[PARTITION_KEY])
    print("All items deleted.")

"""
az cosmosdb sql container merge \
    --resource-group 'allekim-testing-rg' \
    --account-name 'allekim-test-sm' \
    --database-name 'Multi-partition-db' \
    --name 'Multi-partition-col'
"""
@pytest.mark.cosmosQuery
class TestPartitionMergeQuery(unittest.TestCase):
    database: DatabaseProxy = None
    container: ContainerProxy = None
    client: cosmos_client.CosmosClient = None
    configs = test_config.TestConfig
    host = configs.host
    masterKey = configs.masterKey
    throughput = configs.THROUGHPUT_FOR_5_PARTITIONS
    throughput_after_merge = configs.THROUGHPUT_FOR_1_PARTITION
    TEST_DATABASE_ID = "Multi-partition-db"
    TEST_CONTAINER_ID = "Multi-partition-col"
    expected_num_partitions = 1

    @classmethod
    def setUpClass(cls):
        cls.client = cosmos_client.CosmosClient(cls.host, cls.masterKey)
        cls.database = cls.client.create_database_if_not_exists(cls.TEST_DATABASE_ID)
        cls.partition_key = PartitionKey(path="/pk")
        cls.container = cls.database.create_container_if_not_exists(
            id=cls.TEST_CONTAINER_ID,
            partition_key=cls.partition_key,
            offer_throughput=cls.throughput
        )

        # # case 2: items existed in each partition
        # target_num_items = 10  # more items?
        # cls.created_item = create_items(cls.container, target_num_items)
        # check_distribution(cls.container)

        # # case 3: some items existed in some partitions, but not all partitions
        # target_num_items = 100  # more items?
        # cls.created_item = create_items(cls.container, target_num_items, [19, 19, 0, 1, 1])
        # check_distribution(cls.container)

        target_throughput = cls.configs.THROUGHPUT_FOR_1_PARTITION
        cls.container.replace_throughput(target_throughput)

    # In the middle of merge
    # case 1: no item existed in each partition
    # case 2: items existed in each partition
    # case 3: some items existed in some partitions, but not all partitions


    from azure.cosmos import http_constants

    def test_read(self):
        properties = self.container.read()
        assert properties['id'] == self.TEST_CONTAINER_ID
        assert properties['partitionKey'] == self.partition_key

    def test_create_item(self):
        # create items
        target_num_items = 10
        created_items = create_items(self.container, target_num_items)

        # verify created items
        for item in created_items:
            actual_item = self.container.read_item(item=item['id'], partition_key=item['pk'])
            assert actual_item['id'] == item['id']
            assert actual_item['pk'] == item[PARTITION_KEY]
            assert actual_item['attr1'] == item['attr1']

    def test_read_item(self):
        created_items = create_items(self.container, 10)
        attributes = ['id', PARTITION_KEY, 'attr1']
        for expected_item in created_items:
            actual_item = self.container.read_item(item=expected_item, partition_key=expected_item[PARTITION_KEY])
            for attr in attributes:
                assert attr in actual_item, f"Attribute {attr} not found in the item."
                assert actual_item[attr] == expected_item[attr], f"Expected {expected_item[attr]} for {attr}, but got {actual_item[attr]}."

    def test_read_all_items(self):
        # read_all_items: first read all and delete all items, and run read all to check if all items were deleted
        all_items = list(self.container.read_all_items())

        # delete items
        for expected_item in all_items:
            self.container.delete_item(item=expected_item['id'], partition_key=expected_item[PARTITION_KEY])

        # read all items again to check if all items were deleted
        all_items_after_delete = list(self.container.read_all_items())
        assert len(all_items_after_delete) == 0, "All items should be deleted, but found some items."

    def test_read_all_items_workflow_test(self):
        # read all items again to check if all items were deleted
        iter_items = self.container.read_all_items()
        for item in iter_items:
            print(item)

    # add test to certain partiton
    def test_query_items_change_feed(self):
        # store continuation token
        query_iterable = self.container.query_items_change_feed(
            is_start_from_beginning=True,
        )
        items = list(query_iterable)
        continuation1 = self.container.client_connection.last_response_headers['etag']

        # create some items
        num_created_items = 10
        create_items(self.container, num_created_items)

        query_iterable = self.container.query_items_change_feed(
            continuation=continuation1
        )
        iter_list = list(query_iterable)
        assert num_created_items == len(iter_list)

    # add test to certain partiton
    def test_query_items(self):
        # create items
        target_num_items = 10
        create_items(self.container, target_num_items, [19, 0, 1, 6, 7])

        # run queries
        run_queries(self.container, 10)

    # # add test to certain partiton
    # def test_query_items_wf(self):
    #     query = 'SELECT * FROM c'
    #     qlist = list(self.container.query_items(query=query, enable_cross_partition_query=True))
    #     continuation1 = self.container.client_connection.last_response_headers['etag']

    def test_replace_item(self):
        # create items
        target_num_items = 10
        created_items = create_items(self.container, target_num_items)

        # replace items
        for item in created_items:
            new_item_body = {
                'id': item['id'],
                'pk': item[PARTITION_KEY],
                'attr1': item['attr1'],
                'new_attr': 'new_value'
            }
            updated_item = self.container.replace_item(item=item, body=new_item_body)
            assert updated_item['new_attr'] == new_item_body['new_attr']

    def test_upsert_item(self):
        # create items
        target_num_items = 10
        created_items = create_items(self.container, target_num_items)

        # upsert items
        for item in created_items:
            new_item_body = {
                'id': item['id'],
                'pk': item[PARTITION_KEY],
                'attr1': item['attr1'],
                'new_attr': 'new_value'
            }
            upserted_item = self.container.upsert_item(body=new_item_body)
            assert upserted_item['new_attr'] == new_item_body['new_attr']

    def test_patch_item(self):
        # read_all_items: first read all and delete all items, and run read all to check if all items were deleted
        all_items = list(self.container.read_all_items())

        # delete items
        for expected_item in all_items:
            self.container.delete_item(item=expected_item['id'], partition_key=expected_item['pk'])

        items = create_items(self.container, 10)

        operations = [
            {"op": "add", "path": "/attr1", "value": f'Data-{str(uuid.uuid4())}'},
        ]
        for item in items:
            self.container.patch_item(item=item, partition_key=item['pk'],
                                 patch_operations=operations)

    def test_execute_item_batch(self):
        delete_all_items(self.container)

        num_items = 10
        partition_key_value = 1
        batch_operations = []
        for i in range(num_items):
            body = create_body(partition_key_value)
            batch_operations.append(("create", (
                body,
            )))

        self.container.execute_item_batch(batch_operations=batch_operations, partition_key=partition_key_value)

        # Verify that all items were created
        for operation in batch_operations:
            body = operation[1][0]
            item = self.container.read_item(item=body['id'], partition_key=body['pk'])
            assert item['id'] == body['id']
            assert item['pk'] == body['pk']

    # test replacing throughput and get throughput
    def test_replace_throughput(self):
        # store original throughput
        original_throughput = self.container.get_throughput()

        # Replace throughput to merge partitions
        target_throughput = 500
        self.container.replace_throughput(target_throughput)

        # Verify that the throughput was replaced
        throughput = self.container.get_throughput()
        assert throughput.offer_throughput == target_throughput

        # revert to original throughput
        self.container.replace_throughput(original_throughput.offer_throughput)

    def test_read_feed_ranges(self):
        feed_ranges = list(self.container.read_feed_ranges())
        print("Number of feed ranges: {}".format(len(feed_ranges)))

        # target_num_feed_ranges = 1 # expect 1 feed range after merge
        assert len(feed_ranges) == self.expected_num_partitions

    def test_delete_all_items_by_partition_key(self):
        # create items
        target_num_items = 100
        created_items = create_items(self.container, target_num_items)
        # created_items = create_items(self.container, target_num_items, DEFAULT_PARTITION_KEY_VALUES[:2])

        # delete_all_items_by_partition_key
        for pk_value in DEFAULT_PARTITION_KEY_VALUES[:1]:
        # for pk_value in DEFAULT_PARTITION_KEY_VALUES:
            print(f"Deleting all items with partition key value: {pk_value}")
            self.container.delete_all_items_by_partition_key(pk_value)


if __name__ == "__main__":
    unittest.main()

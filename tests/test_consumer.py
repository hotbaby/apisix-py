# encoding: utf8

import os
import time
import datetime
import unittest
from apisix.admin import ConsumerAPI

from . import config


class TestConsumerAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.consumer_api = ConsumerAPI(domain=config.DOMAIN,
                                        username=config.USERNAME,
                                        password=config.PASSWORD)

    def test_list_consumers(self):
        resp = self.consumer_api.list()
        assert resp['code'] == 0
        print(resp)

    def test_retrieve_consumer(self):
        consumers = self.consumer_api.list()
        consumer = consumers['data']['rows'][0]

        resp = self.consumer_api.retrieve(consumer['username'])
        print(resp)
        assert resp['code'] == 0
        assert resp['data']['username'] == consumer['username']

    def test_update_consumer(self):
        consumers = self.consumer_api.list()
        consumer = consumers['data']['rows'][0]

        resp = self.consumer_api.retrieve(consumer['username'])
        consumer = resp['data']
        consumer.pop('create_time')
        consumer.pop('update_time')
        resp = self.consumer_api.update(consumer['username'], consumer)
        print(resp)
        assert resp['code'] == 0

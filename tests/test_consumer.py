# encoding: utf8

import os
import time
import datetime
import unittest
from apisix.admin import ConsumerAPI

DOMAIN = 'http://apisix.ai-test.speechocean.com'
USERNAME = 'admin'
PASSWORD = os.environ.get('APISIX_PASSWORD')
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class TestConsumerAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.consumer_api = ConsumerAPI(domain=DOMAIN, username=USERNAME, password=PASSWORD)

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
        consumer['desc'] = f'{datetime.datetime.now().strftime(DATETIME_FORMAT)}'
        resp = self.consumer_api.update(consumer['username'], consumer)
        print(resp)
        assert resp['code'] == 0

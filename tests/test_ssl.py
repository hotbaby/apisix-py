# encoding: utf8


import os
import json
import time
import datetime
import unittest
from apisix.admin import SSLAPI

DOMAIN = 'http://apisix.ai-test.speechocean.com'
USERNAME = 'admin'
PASSWORD = os.environ.get('APISIX_PASSWORD')
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class TestUpstream(unittest.TestCase):
    def setUp(self) -> None:
        self.ssl_api = SSLAPI(domain=DOMAIN, username=USERNAME, password=PASSWORD)

    def test_list_ssl(self):
        resp = self.ssl_api.list_ssl()
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_retrieve_ssl(self):
        resp = self.ssl_api.list_ssl()
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

        ssl = resp['data']['rows'][0]
        resp = self.ssl_api.retrieve_ssl(ssl['id'])
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_update_ssl(self):
        resp = self.ssl_api.list_ssl()
        assert resp['code'] == 0

        ssl = resp['data']['rows'][0]
        resp = self.ssl_api.retrieve_ssl(ssl['id'])
        assert resp['code'] == 0
        ssl = resp['data']

        ssl['update_time'] = int(time.time())
        resp = self.ssl_api.update_ssl(ssl['id'], ssl)
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

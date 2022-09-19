# encoding: utf8


import os
import json
import time
import datetime
import unittest
from apisix.admin import SSLAPI

from . import config


class TestSSLAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.ssl_api = SSLAPI(domain=config.DOMAIN,
                              username=config.USERNAME,
                              password=config.PASSWORD)

    def test_list_ssl(self):
        resp = self.ssl_api.list()
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_retrieve_ssl(self):
        resp = self.ssl_api.list()
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

        ssl = resp['data']['rows'][0]
        resp = self.ssl_api.retrieve(ssl['id'])
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_update_ssl(self):
        resp = self.ssl_api.list()
        assert resp['code'] == 0

        ssl = resp['data']['rows'][0]
        resp = self.ssl_api.retrieve(ssl['id'])
        assert resp['code'] == 0
        ssl = resp['data']

        ssl['update_time'] = int(time.time())
        resp = self.ssl_api.update(ssl['id'], ssl)
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

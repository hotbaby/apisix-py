# encoding: utf8


import os
import json
import time
import datetime
import unittest
from apisix.admin import UpstreamAPI

from . import config


class TestUpstreamAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream_api = UpstreamAPI(domain=config.DOMAIN,
                                        username=config.USERNAME,
                                        password=config.PASSWORD)

    def test_list_upstreams(self):
        resp = self.upstream_api.list()
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_retrieve_upstream(self):
        resp = self.upstream_api.list()
        upstream = resp['data']['rows'][0]

        resp = self.upstream_api.retrieve(upstream['id'])
        print(json.dumps(resp, ensure_ascii=False))
        assert resp['code'] == 0

    def test_update_upstream(self):
        resp = self.upstream_api.list()
        upstream = resp['data']['rows'][0]

        resp = self.upstream_api.retrieve(upstream['id'])
        print(json.dumps(resp, ensure_ascii=False))
        assert resp['code'] == 0
        upstream = resp['data']

        upstream.pop('update_time')
        upstream.pop('create_time')
        resp = self.upstream_api.update(upstream['id'], upstream)
        print(json.dumps(resp, ensure_ascii=False))
        assert resp['code'] == 0

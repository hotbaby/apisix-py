# encoding: utf8


import os
import json
import time
import datetime
import unittest
from apisix.admin import UpstreamAPI

DOMAIN = 'http://apisix.ai-test.speechocean.com'
USERNAME = 'admin'
PASSWORD = os.environ.get('APISIX_PASSWORD')
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class TestUpstream(unittest.TestCase):
    def setUp(self) -> None:
        self.upstream_api = UpstreamAPI(domain=DOMAIN, username=USERNAME, password=PASSWORD)

    def test_list_upstreams(self):
        resp = self.upstream_api.list_upstreams()
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_retrieve_upstream(self):
        resp = self.upstream_api.list_upstreams()
        upstream = resp['data']['rows'][0]

        resp = self.upstream_api.retrieve_upstream(upstream['id'])
        print(json.dumps(resp, ensure_ascii=False))
        assert resp['code'] == 0

    def test_update_upstream(self):
        resp = self.upstream_api.list_upstreams()
        upstream = resp['data']['rows'][0]

        resp = self.upstream_api.retrieve_upstream(upstream['id'])
        print(json.dumps(resp, ensure_ascii=False))
        assert resp['code'] == 0
        upstream = resp['data']

        upstream['update_time'] = int(time.time())
        resp = self.upstream_api.update_upstream(upstream['id'], upstream)
        print(json.dumps(resp, ensure_ascii=False))
        assert resp['code'] == 0

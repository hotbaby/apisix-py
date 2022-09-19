# encoding: utf8
import json
import os
import time
import datetime
import unittest
from apisix.admin import RouteAPI

DOMAIN = 'http://apisix.ai-test.speechocean.com'
USERNAME = 'admin'
PASSWORD = os.environ.get('APISIX_PASSWORD')
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class TestConsumer(unittest.TestCase):
    def setUp(self) -> None:
        self.route_api = RouteAPI(domain=DOMAIN, username=USERNAME, password=PASSWORD)

    def test_list_routes(self):
        resp = self.route_api.list_routes()
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_retrieve_route(self):
        resp = self.route_api.list_routes()
        assert resp['code'] == 0
        route = resp['data']['rows'][0]

        resp = self.route_api.retrieve_route(route['id'])
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_update_route(self):
        resp = self.route_api.list_routes()
        assert resp['code'] == 0
        route = resp['data']['rows'][0]

        resp = self.route_api.retrieve_route(route['id'])
        assert resp['code'] == 0
        route = resp['data']

        route['update_time'] = int(time.time())
        resp = self.route_api.update_route(route['id'], route)
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

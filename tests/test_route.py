# encoding: utf8

import json
import os
import time
import datetime
import unittest
from apisix.admin import RouteAPI

from . import config


class TestRouteAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.route_api = RouteAPI(domain=config.DOMAIN,
                                  username=config.USERNAME,
                                  password=config.PASSWORD)

    def test_list_routes(self):
        resp = self.route_api.list()
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_retrieve_route(self):
        resp = self.route_api.list()
        assert resp['code'] == 0
        route = resp['data']['rows'][0]

        resp = self.route_api.retrieve(route['id'])
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_update_route(self):
        resp = self.route_api.list()
        assert resp['code'] == 0
        route = resp['data']['rows'][0]

        resp = self.route_api.retrieve(route['id'])
        assert resp['code'] == 0
        route = resp['data']

        route['update_time'] = int(time.time())
        route.pop('create_time')
        route.pop('update_time')
        resp = self.route_api.update(route['id'], route)
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

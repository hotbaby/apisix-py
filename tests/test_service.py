# encoding: utf8


import os
import json
import time
import datetime
import unittest
from apisix.admin import ServiceAPI

from . import config


class TestServiceAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.service_api = ServiceAPI(domain=config.DOMAIN,
                                      username=config.USERNAME,
                                      password=config.PASSWORD)

    def test_list_services(self):
        resp = self.service_api.list()
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_retrieve_service(self):
        resp = self.service_api.list()
        assert resp['code'] == 0
        service = resp['data']['rows'][0]

        resp = self.service_api.retrieve(service['id'])
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_update_service(self):
        resp = self.service_api.list()
        assert resp['code'] == 0
        service = resp['data']['rows'][0]

        resp = self.service_api.retrieve(service['id'])
        assert resp['code'] == 0
        service = resp['data']
        print(json.dumps(resp, ensure_ascii=False))

        service['update_time'] = int(time.time())
        resp = self.service_api.update(service['id'], service)
        assert resp['code'] == 0
# encoding: utf8


import os
import json
import time
import datetime
import unittest
from apisix.admin import ServiceAPI

DOMAIN = 'http://apisix.ai-test.speechocean.com'
USERNAME = 'admin'
PASSWORD = os.environ.get('APISIX_PASSWORD')
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class TestUpstream(unittest.TestCase):
    def setUp(self) -> None:
        self.service_api = ServiceAPI(domain=DOMAIN, username=USERNAME, password=PASSWORD)

    def test_list_services(self):
        resp = self.service_api.list_services()
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_retrieve_service(self):
        resp = self.service_api.list_services()
        assert resp['code'] == 0
        service = resp['data']['rows'][0]

        resp = self.service_api.retrieve_service(service['id'])
        assert resp['code'] == 0
        print(json.dumps(resp, ensure_ascii=False))

    def test_update_service(self):
        resp = self.service_api.list_services()
        assert resp['code'] == 0
        service = resp['data']['rows'][0]

        resp = self.service_api.retrieve_service(service['id'])
        assert resp['code'] == 0
        service = resp['data']
        print(json.dumps(resp, ensure_ascii=False))

        service['update_time'] = int(time.time())
        resp = self.service_api.update_service(service['id'], service)
        assert resp['code'] == 0
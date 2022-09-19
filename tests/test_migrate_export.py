# encoding: utf8

import os
import time
import datetime
import unittest
from apisix.admin import MigrateAPI

DOMAIN = 'http://apisix.ai-test.speechocean.com'
USERNAME = 'admin'
PASSWORD = os.environ.get('APISIX_PASSWORD')
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class TestMigrateExportAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.migrate_api = MigrateAPI(domain=DOMAIN, username=USERNAME, password=PASSWORD)

    def test_export_data(self):
        self.migrate_api.export_data('./migrate')

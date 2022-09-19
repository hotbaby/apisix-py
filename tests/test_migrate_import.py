# encoding: utf8

import os
import time
import datetime
import unittest
from apisix.admin import MigrateAPI

DOMAIN = 'http://localhost:9000'
USERNAME = 'admin'
PASSWORD = 'admin'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class TestMigrateImportAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.migrate_api = MigrateAPI(domain=DOMAIN, username=USERNAME, password=PASSWORD)

    def test_import_data(self):
        self.migrate_api.import_data('./migrate')

# encoding: utf8

import os
import time
import datetime
import unittest
from apisix.admin import MigrateAPI

from . import config


class TestMigrateExportAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.migrate_api = MigrateAPI(domain=config.DOMAIN,
                                      username=config.USERNAME,
                                      password=config.PASSWORD)

    def test_export_data(self):
        self.migrate_api.export_data('./migrate')

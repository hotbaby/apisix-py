# encoding: utf8

import os
import time
import datetime
import unittest
from apisix.admin import MigrateAPI

from . import config


class TestMigrateImportAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.migrate_api = MigrateAPI(domain=config.DOMAIN,
                                      username=config.USERNAME,
                                      password=config.PASSWORD)

    # def test_import_data(self):
    #     self.migrate_api.import_data('./migrate')

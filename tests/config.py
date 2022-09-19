# encoding: utf8

import os

DOMAIN = os.environ.get('APISIX_DOMAIN')
USERNAME = 'admin'
PASSWORD = os.environ.get('APISIX_PASSWORD')
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

print(f'domain: {DOMAIN} \n'
      f'username: {USERNAME} \n'
      f'password: {PASSWORD}')

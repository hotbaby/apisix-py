# encoding: utf8

import enum
import json
import os.path
import pathlib
from urllib.parse import urljoin

import requests


class APISIXException(Exception):
    pass


class HTTPMethod(enum.Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


def check_login(func):
    def wrapper(self, *args, **kwargs):
        if not self.token:
            self.login()

        return func(self, *args, **kwargs)

    return wrapper


class AdminAPIBase:

    def __init__(self, domain: str, username: str, password: str):
        self.domain = domain
        self.username = username
        self.password = password
        self.token = None

    def login(self):
        path = '/apisix/admin/user/login'
        url = urljoin(self.domain, path)
        data = {
            'username': self.username,
            'password': self.password
        }

        resp_json = self.request(HTTPMethod.POST.value, url, data=data)
        assert resp_json['code'] == 0, f'login error, url: {url}, data: {json.dumps(data)},' \
                                       f' resp: {json.dumps(resp_json)}'
        self.token = resp_json['data']['token']

    def request(self, method: str, url: str, data: dict = None, **kwargs):
        headers = {}
        if self.token:
            headers['Authorization'] = self.token

        if method == HTTPMethod.GET.value:
            resp = requests.get(url, headers=headers)
        elif method == HTTPMethod.POST.value:
            resp = requests.post(url, json=data, headers=headers)
        elif method == HTTPMethod.PUT.value:
            resp = requests.put(url, json=data, headers=headers)
        elif method == HTTPMethod.DELETE.value:
            resp = requests.delete(url, headers=headers)
        else:
            assert f'Unknown http method {method}!'

        if resp.status_code != 200:
            raise APISIXException(f'request error, url: {url}, method:{method}, data: {data}, '
                                  f'resp_status_code: {resp.status_code}, resp_text: {resp.text}')

        return resp.json()

    @check_login
    def get(self, url: str):
        return self.request(HTTPMethod.GET.value, url=url)

    @check_login
    def post(self, url: str, data: dict):
        return self.request(HTTPMethod.POST.value, url=url, data=data)

    @check_login
    def put(self, url: str, data: dict):
        return self.request(HTTPMethod.PUT.value, url=url, data=data)

    @check_login
    def delete(self, url: str):
        return self.request(HTTPMethod.DELETE.value, url=url)


class ConsumerAPI(AdminAPIBase):
    name = 'consumer'
    id_name = 'username'

    def list(self):
        path = '/apisix/admin/consumers'
        url = urljoin(self.domain, path)
        return self.get(url)

    def retrieve(self, consumer_id: str):
        path = f'/apisix/admin/consumers/{consumer_id}'
        url = urljoin(self.domain, path)
        return self.get(url)

    def update(self, consumer_id: str, data: dict):
        path = f'/apisix/admin/consumers/{consumer_id}'
        url = urljoin(self.domain, path)
        return self.put(url, data=data)

    def delete(self, consumer_id: str, data: dict):
        path = f'/apisix/admin/consumers/{consumer_id}'
        url = urljoin(self.domain, path)
        return self.delete(url)


class UpstreamAPI(AdminAPIBase):

    name = 'upstream'
    id_name = 'id'

    def list(self):
        path = '/apisix/admin/upstreams'
        url = urljoin(self.domain, path)
        return self.get(url)

    def retrieve(self, upstream_id: str):
        path = f'/apisix/admin/upstreams/{upstream_id}'
        url = urljoin(self.domain, path)
        return self.get(url)

    def update(self, upstream_id: str, data: dict):
        path = f'/apisix/admin/upstreams/{upstream_id}'
        url = urljoin(self.domain, path)
        return self.put(url, data)


class ServiceAPI(AdminAPIBase):

    name = 'service'
    id_name = 'id'

    def list(self):
        path = '/apisix/admin/services'
        url = urljoin(self.domain, path)
        return self.get(url)

    def retrieve(self, service_id: str):
        path = f'/apisix/admin/services/{service_id}'
        url = urljoin(self.domain, path)
        return self.get(url)

    def update(self, service_id: str, data: dict):
        path = f'/apisix/admin/services/{service_id}'
        url = urljoin(self.domain, path)
        return self.put(url, data)


class RouteAPI(AdminAPIBase):

    name = 'route'
    id_name = 'id'

    def list(self):
        path = '/apisix/admin/routes'
        url = urljoin(self.domain, path)
        return self.get(url)

    def retrieve(self, route_id: str):
        path = f'/apisix/admin/routes/{route_id}'
        url = urljoin(self.domain, path)
        return self.get(url)

    def update(self, route_id: str, data: dict):
        path = f'/apisix/admin/routes/{route_id}'
        url = urljoin(self.domain, path)
        return self.put(url, data)


class SSLAPI(AdminAPIBase):

    name = 'ssl'
    id_name = 'id'

    def list(self):
        path = '/apisix/admin/ssl'
        url = urljoin(self.domain, path)
        return self.get(url)

    def retrieve(self, ssl_id: str):
        path = f'/apisix/admin/ssl/{ssl_id}'
        url = urljoin(self.domain, path)
        return self.get(url)

    def update(self, ssl_id: str, data: dict):
        path = f'/apisix/admin/ssl/{ssl_id}'
        url = urljoin(self.domain, path)
        return self.put(url, data)


class MigrateAPI(AdminAPIBase):

    def export_data(self, config_path: str):
        apis = [
            # SSLAPI(self.domain, self.username, self.password),
            UpstreamAPI(self.domain, self.username, self.password),
            ServiceAPI(self.domain, self.username, self.password),
            RouteAPI(self.domain, self.username, self.password),
            ConsumerAPI(self.domain, self.username, self.password)
        ]

        for api in apis:
            for row in api.list()['data']['rows']:
                resp = api.retrieve(row[api.id_name])
                assert resp['code'] == 0

                path = os.path.join(config_path, api.name, f'{api.name}-{row[api.id_name]}.json')
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))

                with open(path, 'w') as f:
                    f.write(json.dumps(resp['data'], ensure_ascii=False))

                print(f'export {os.path.basename(path)} successfully')

    def import_data(self, config_path: str):
        apis = [
            # SSLAPI(self.domain, self.username, self.password),
            UpstreamAPI(self.domain, self.username, self.password),
            ServiceAPI(self.domain, self.username, self.password),
            RouteAPI(self.domain, self.username, self.password),
            ConsumerAPI(self.domain, self.username, self.password)
        ]

        p = pathlib.Path(config_path)
        for api in apis:
            for item in list(p.glob(f'{api.name}/*.json')):
                with open(str(item)) as f:
                    data = json.load(f)

                    # bugfix {"code":10000,"message":"we don't accept create_time from client"}
                    data.pop('create_time')
                    data.pop('update_time')

                    api.update(data[api.id_name], data)

                    print(f'import {item.name} successfully')

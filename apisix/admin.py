# encoding: utf8

import enum
import json
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
            raise APISIXException(f'request error, url: {url}, method:{method}, data: {data}, resp: {resp}')

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

    def list_consumers(self):
        path = '/apisix/admin/consumers'
        url = urljoin(self.domain, path)
        return self.get(url)

    def retrieve_consumer(self, consumer_id: str):
        path = f'/apisix/admin/consumers/{consumer_id}'
        url = urljoin(self.domain, path)
        return self.get(url)

    def update_consumer(self, consumer_id: str, data: dict):
        path = f'/apisix/admin/consumers/{consumer_id}'
        url = urljoin(self.domain, path)
        return self.put(url, data=data)

    def delete_consumer(self, consumer_id: str, data: dict):
        path = f'/apisix/admin/consumers/{consumer_id}'
        url = urljoin(self.domain, path)
        return self.delete(url)


class UpstreamAPI(AdminAPIBase):

    def list_upstreams(self):
        path = '/apisix/admin/upstreams'
        url = urljoin(self.domain, path)
        return self.get(url)

    def retrieve_upstream(self, upstream_id: str):
        path = f'/apisix/admin/upstreams/{upstream_id}'
        url = urljoin(self.domain, path)
        return self.get(url)

    def update_upstream(self, upstream_id: str, data: dict):
        path = f'/apisix/admin/upstreams/{upstream_id}'
        url = urljoin(self.domain, path)
        return self.put(url, data)


class ServiceAPI(AdminAPIBase):

    def list_services(self):
        path = '/apisix/admin/services'
        url = urljoin(self.domain, path)
        return self.get(url)

    def retrieve_service(self, service_id: str):
        path = f'/apisix/admin/services/{service_id}'
        url = urljoin(self.domain, path)
        return self.get(url)

    def update_service(self, service_id: str, data: dict):
        path = f'/apisix/admin/services/{service_id}'
        url = urljoin(self.domain, path)
        return self.put(url, data)

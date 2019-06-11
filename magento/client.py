import requests
import json
from urllib.parse import urljoin

from .categories import Categories
from .products import Products
from .errors import BadRequestError, UnauthorizedError, UnexpectedError

# installed sub-module
installed_modules = {
    "categories": Categories,
    "products": Products
}


class ClientMeta(type):
    def __new__(mcs, name, bases, dct):
        klass = super(ClientMeta, mcs).__new__(mcs, name, bases, dct)
        setattr(
            klass, "installed_modules",
            installed_modules
        )
        return klass


class Client(object, metaclass=ClientMeta):
    cached_modules = {}

    def __init__(self, url, access_token, version="V1"):
        self.access_token = access_token
        self.url = url
        self.api_version = version
        self.session = requests.Session()

    def __getattr__(self, name):
        try:
            value = super().__getattribute__(name)
        except AttributeError as e:
            value = self.get_cached_module(name)
            if not value:
                raise e
        return value

    def get_cached_module(self, key):
        cache_key = self.url + key

        cached_module = self.cached_modules.get(cache_key)

        if not cached_module:
            installed = self.installed_modules.get(key)
            if not installed:
                return None
            cached_module = installed(self)
            self.cached_modules.setdefault(cache_key, cached_module)
        return cached_module

    def build_request(self, method, uri, params=None):
        method = method.upper()
        url = urljoin(self.url, "rest/%s/%s" % (self.api_version, uri,))

        headers = {
            "Authorization": "Bearer %s" % self.access_token
        }
        req = requests.Request(method, url, headers=headers)

        if params:
            if req.method in ["POST", "PUT", "PATH"]:
                req.json = params
            else:
                req.params = params
        return req

    def build_response(self, resp):
        if resp.headers.get('content-type').split(";")[0] != "application/json":
            resp.raise_for_status()

        if resp.status_code == 200:
            return resp.json()

        elif resp.status_code == 400:
            print(resp.json())
            raise BadRequestError(resp)

        elif resp.status_code == 401:

            raise UnauthorizedError(resp)
        print(resp.json())
        raise UnexpectedError(resp)

    def execute(self, method, uri, params=None):

        req = self.build_request(method, uri, params)
        prepped = req.prepare()
        resp = self.session.send(prepped)

        resp = self.build_response(resp)
        return resp

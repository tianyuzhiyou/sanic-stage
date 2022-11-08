# -*- coding: utf-8 -*-

import functools
import traceback
from typing import Any

import aiohttp

from config import config
from utils.loggers import logger
from drivers.http_client import httpClient

__all__ = [
    'options',
    'head',
    'get',
    'post',
    'put',
    'delete',
    'request',
    'APIClient',
    'join_url',
    "intranet_route"
]


def join_url(base_url, path):
    if base_url.endswith('/'):
        base_url = base_url.rstrip('/')

    if path.startswith('/'):
        path = path.lstrip('/')

    return f'{base_url}/{path}'


async def response_text(response):
    data = await response.text()
    return data


async def response_content(response):
    data = await response.content.read()
    return data


async def response_json(response, return_raw_data=False):
    res = await response.json()
    if return_raw_data:
        return res
    return res.get('data')


async def request(session, method: str, url: str, err_default: Any = None, **kwargs):
    """

    :param session:
    :param method:
    :param url:
    :param err_default: 传参该值后 当请求发生错误时 返回此默认值, 不传此值请求错误后返回dict
    :param kwargs:
    """
    headers = kwargs.get('headers', {})

    if 'project' not in headers:
        headers['project'] = config.PROJECT_NAME
    kwargs['headers'] = headers

    return_raw_data = kwargs.pop('return_raw_data', False)
    response_type = kwargs.pop('response_type', "json")

    timeout = kwargs.pop('timeout', config.REQUEST_TIMEOUT)
    kwargs['timeout'] = aiohttp.ClientTimeout(total=timeout)

    try:
        async with session.request(method, url, **kwargs) as response:
            if response.status != 200:
                response.raise_for_status()

            if response_type == "text":
                data = await response_text(response)
            elif response_type == "content":
                data = await response_content(response)
            else:
                data = await response_json(response, return_raw_data)

    except Exception as e:
        error = traceback.format_exc()
        logger.error(f'http error: {e=}, {method=}, {url=}, {kwargs=}, {error=}')

        if err_default is not None:
            data = err_default
            return data
        else:
            raise e  # 抛出异常，不能吃掉异常，否则可能有无法预知的问题
    else:
        return data


async def options(url: str, **kwargs):
    res = await request(httpClient.client, 'OPTIONS', url, **kwargs)
    return res


async def head(url: str, **kwargs):
    res = await request(httpClient.client, 'HEAD', url, **kwargs)
    return res


async def get(url: str, params: dict = None, json: dict = None, **kwargs):
    res = await request(httpClient.client, 'GET', url, params=params, json=json, **kwargs)
    return res


async def post(url: str, data: dict = None, json: dict = None, **kwargs):
    res = await request(httpClient.client, 'POST', url, data=data, json=json, **kwargs)
    return res


async def put(url: str, data: dict = None, json: dict = None, **kwargs):
    res = await request(httpClient.client, 'PUT', url, data=data, json=json, **kwargs)
    return res


async def patch(url: str, data: dict = None, json: dict = None, **kwargs):
    res = await request(httpClient.client, 'PATCH', url, data=data, json=json, **kwargs)
    return res


async def delete(url: str, params: dict = None, **kwargs):
    res = await request(httpClient.client, 'DELETE', url, params=params, **kwargs)
    return res


class APIClient:
    """
    # 01
    from utils.api_client import APIClient
    class XService:
        def __init__(self):
            self.api = APIClient(endpoint_name='EXAMPLE')

        async def do_sth(self):
            url = self.api.make_url(path)
            res = await self.api.get(url, params=params)
            return res

    # 02
    from utils import api_client
    async def do_sth():
        url = 'http://api.example.com/prefix/path/'
        res = await api_client.get(url, params=params)
        return res

    # 03
    from utils import api_client
    async def do_sth():
        url = api_client.join_url(base_url='http://api.example.com/prefix/', path)
        res = await api_client.get(url, params=params)
        return res
    """

    def __init__(self, endpoint_name: str):
        self.endpoint_name = endpoint_name

    def make_url(self, path: str) -> str:
        base_url = config.ENDPOINTS.get(self.endpoint_name, "")
        return join_url(base_url, path)

    async def request(self, session, method: str, url: str, **kwargs):
        res = await request(session, method, url, **kwargs)
        return res

    async def options(self, url: str, **kwargs):
        res = await options(url, **kwargs)
        return res

    async def head(self, url: str, **kwargs):
        res = await head(url, **kwargs)
        return res

    async def get(self, url: str, params: dict = None, json: dict = None, **kwargs):
        res = await get(url, params=params, json=json, **kwargs)
        return res

    async def post(self, url: str, data: dict = None, json: dict = None, **kwargs):
        res = await post(url, data=data, json=json, **kwargs)
        return res

    async def put(self, url: str, data: dict = None, json: dict = None, **kwargs):
        res = await put(url, data=data, json=json, **kwargs)
        return res

    async def patch(self, url: str, data: dict = None, json: dict = None, **kwargs):
        res = await patch(url, data=data, json=json, **kwargs)
        return res

    async def delete(self, url: str, params: dict = None, **kwargs):
        res = await delete(url, params=params, **kwargs)
        return res


def intranet_route(client: APIClient, base_url: str, method: str = "POST"):
    """
    @desc　封装内部接口调用
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        async def new_func(*args, **kwargs):
            url = client.make_url(base_url)
            params = await func(*args, **kwargs)
            if str(method).upper() == "POST":
                res = await client.post(url, json=params)
            else:
                res = await client.get(url, params=params)
            return res

        return new_func

    return decorator

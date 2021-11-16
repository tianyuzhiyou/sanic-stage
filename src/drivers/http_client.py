# -*- coding: utf-8 -*-

"""定义http请求全局初始化, 目的是较少aiohttp.ClientSession对象的创建，防止高并发情况下连接被耗尽"""

import aiohttp
import asyncio
import sanic
from config import config


class HttpClient(object):
    FormData = aiohttp.FormData
    headers = {
        "Content-Type": "application/json;charset=utf-8"
    }
    client: aiohttp.ClientSession = None

    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

    @staticmethod
    def new_client() -> aiohttp.ClientSession:
        client = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                limit=config["HTTP_REQUEST_CONCURRENCY_LIMIT"],
                loop=asyncio.get_running_loop()
            ),
            loop=asyncio.get_running_loop()
        )
        return client

    async def init_client(self):
        session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                limit=config["HTTP_REQUEST_CONCURRENCY_LIMIT"],
                loop=self.loop
            ),
            loop=self.loop
        )
        setattr(HttpClient, "client", session)  # 全局session对象
        self.client = session  # 使用对象引用住，便于关闭
        return session


httpClient = HttpClient


async def init_http(app: sanic.app, loop: asyncio.AbstractEventLoop):
    """app启动之前初始化http对象,作为应用上下文存在"""
    app.http_client = HttpClient(loop)
    asyncio.ensure_future(app.http_client.init_client(), loop=loop)


async def close_http(app: sanic.app, loop: asyncio.AbstractEventLoop):
    """服务停止时关闭http连接池"""
    if app.http_client.client:
        await app.http_client.client.close()


async def init_http_for_celery():
    """初始化celery的http"""
    loop = asyncio.get_running_loop()
    http_client = HttpClient(loop)
    await http_client.init_client()
    setattr(loop, "http_client", http_client)


async def close_http_for_celery():
    """关闭celery的http连接池"""
    loop = asyncio.get_running_loop()
    http_client: HttpClient = getattr(loop, "http_client", None)
    if http_client is not None:
        await http_client.client.close()

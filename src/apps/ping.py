# -*- coding: utf-8 -*-

"""
ping监控接口
"""
from sanic.views import HTTPMethodView
from sanic import response

from business import biz
from utils.loggers import logger
from tasks.tests import celery_test


class PingView(HTTPMethodView):

    async def get(self, request):
        res = await biz.ping.ping()
        return response.text(res)


class PingRedisView(HTTPMethodView):

    async def get(self, request):
        res = await biz.ping.ping_redis()
        return response.text(res)


class PingMysqlView(HTTPMethodView):

    async def get(self, request):
        res = await biz.ping.ping_mysql()
        return response.text(res)


class LoggerView(HTTPMethodView):

    async def get(self, request):
        msg = "测试日志配置成功！"
        logger.info(msg)
        return response.text("OK")


class SentryView(HTTPMethodView):

    async def get(self, request):
        """测试sentry"""
        raise Exception("测试sentry发送！")


class PingCeleryView(HTTPMethodView):
    async def get(self, request):
        """测试celery"""
        await celery_test.delay()
        return response.text("OK")

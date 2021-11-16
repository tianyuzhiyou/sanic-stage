# -*- coding:utf-8 -*-

from services import svc


class PingBusiness(object):

    async def ping(self):
        await svc.ping.ping_redis()
        await svc.ping.ping_mysql()
        return 'success'

    async def ping_redis(self):
        await svc.ping.ping_redis()
        return "PONG"

    async def ping_mysql(self):
        await svc.ping.ping_mysql()
        return "PONG"

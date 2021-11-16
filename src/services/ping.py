# -*- coding:utf-8 -*-

from drivers.redis import redis_db
from drivers.mysql import db

__all__ = ['PingService']


class PingService(object):

    async def ping_redis(self):
        result = await redis_db.common.ping()
        assert result == "PONG"
        return "success"

    async def ping_mysql(self):
        stmt = "select 42;"
        async with db.db.acquire() as conn:
            cursor = await conn.execute(stmt)
            mysql_res = await cursor.scalar()
        assert mysql_res == 42
        return "success"

    async def ping(self):
        await self.ping_redis()
        await self.ping_mysql()
        return "success"



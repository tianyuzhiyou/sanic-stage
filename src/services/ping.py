# -*- coding:utf-8 -*-

from drivers.redis import redis_db
from drivers.mysql import db
import aiotask_context as context

__all__ = ['PingService']


class PingService(object):

    async def ping_redis(self):
        app = context.get("app")
        if app.config.get("ENABLE_REDIS", False) and app.config["REDIS_CONFIG"].get("default", {}):
            result = await redis_db.common.ping()
            assert result == "PONG"
        return "success"

    async def ping_mysql(self):
        app = context.get("app")
        if app.config.get("ENABLE_DB", False) and app.config.get("MYSQL_CONFIG", {}).get("default"):
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



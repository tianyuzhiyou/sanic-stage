"""
@desc: redis 数据库入口
"""
from functools import lru_cache

import aioredis
from sanic import Sanic
from cached_property import cached_property


@lru_cache(maxsize=2000)
def redis_get_conf(name: str, app) -> dict:
    """ get config by env name
    :param name: default/
    :return: dict
    """
    conf = app.config["REDIS_CONFIG"][name]
    return dict(
        address=conf["address"],
        maxsize=conf["maxsize"],
        db=conf.get("db", 0),
        password=conf.get("password", None),
        minsize=conf["minsize"],
        timeout=conf["timeout"],
        encoding=conf["encoding"]
    )


class RedisCache:

    def __init__(self):
        self.common = None

    @cached_property
    async def common_redis(self) -> aioredis.ConnectionsPool:
        pool = await aioredis.create_redis_pool(**redis_get_conf("default", self.app))
        return pool

    async def init_redis_cache(self, app: Sanic):
        if app.config["REDIS_CONFIG"].get("default", {}):
            self.app = app
            self.common = await self.common_redis

    async def init_redis_for_celery(self, app):
        """celery连接redis初始化"""
        if app.config["REDIS_CONFIG"].get("default", {}):
            self.app = app
            self.common = await self.common_redis

    async def close_redis_cache(self):
        if self.common:
            self.common.close()
            await self.common.wait_closed()


redis_db = RedisCache()

__all__ = ['redis_db']

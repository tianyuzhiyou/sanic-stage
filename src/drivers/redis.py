"""
@desc: redis 数据库入口
"""
from functools import lru_cache

import aioredis
from sanic import Sanic
from cached_property import cached_property
from utils.loggers import logger


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
        if not app.config.get("ENABLE_REDIS", False) or not app.config["REDIS_CONFIG"].get("default", {}):
            logger.info("当前未启用redis连接设置或未配置redis连接参数，无法连接redis...")
            return
        self.app = app
        self.common = await self.common_redis
        logger.info("连接redis成功...")

    async def init_redis_for_celery(self, app):
        """celery连接redis初始化"""
        if not app.config.get("ENABLE_REDIS", False) or not app.config["REDIS_CONFIG"].get("default", {}):
            logger.info("当前未启用redis连接设置或未配置redis连接参数，无法连接redis...")
            return
        self.app = app
        self.common = await self.common_redis
        logger.info("连接redis成功...")

    async def close_redis_cache(self):
        if self.common:
            self.common.close()
            await self.common.wait_closed()
            logger.info("已成功关闭redis连接...")


redis_db = RedisCache()

__all__ = ['redis_db']

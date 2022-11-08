"""mysql连接工具"""

from sanic import Sanic
from aiomysql import sa
from cached_property import cached_property
from utils.loggers import logger


def get_db_config(name: str = "default", app: Sanic = None) -> dict:
    conf = app.config["MYSQL_CONFIG"][name]
    return dict(
        minsize=conf["pool_min_size"],
        maxsize=conf["pool_max_size"],
        host=conf["host"],
        port=conf["port"],
        user=conf["user"],
        password=conf["password"],
        db=conf["db"],
        autocommit=conf["autocommit"]
    )


class DB:

    @cached_property
    async def default_db(self) -> sa.Engine:
        engine = await sa.create_engine(**get_db_config("default", self.app))
        return engine

    def __init__(self):
        self.db = None

    async def init_db(self, app: Sanic):
        if not app.config.get("ENABLE_DB", False) or not app.config.get("MYSQL_CONFIG", {}).get("default"):
            logger.info("当前未启用db连接设置或未配置db连接参数，无法连接db...")
            return
        self.app = app
        self.db = await self.default_db
        logger.info("连接mysql成功...")

    async def close_db(self):
        self.db.close()
        await self.db.wait_closed()
        logger.info("关闭redis成功...")


db = DB()

__all__ = ['db']

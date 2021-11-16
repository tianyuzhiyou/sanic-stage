"""mysql连接工具"""

from sanic import Sanic
from aiomysql import sa
from cached_property import cached_property


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
        self.app = app
        self.db = await self.default_db

    async def close_db(self):
        self.db.close()
        await self.db.wait_closed()


db = DB()

__all__ = ['db']

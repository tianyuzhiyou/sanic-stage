# -*- coding: utf-8 -*-

import aiotask_context as context
from sanic import Sanic

from drivers.redis import redis_db
from drivers.mysql import db
from drivers.http_client import init_http, close_http


async def before_serve(app, loop):
    # 服务启动之前
    await init_http(app, loop)


async def setup_serve(app, loop):
    # 服务启动之后处理
    loop.set_task_factory(context.task_factory)

    # 初始化redis
    await redis_db.init_redis_cache(app)

    # init mysql
    await db.init_db(app)


async def teardown_serve(app, loop):
    await redis_db.close_redis_cache()
    await db.close_db()
    await close_http(app, loop)


def register_listeners(app: Sanic):
    app.register_listener(before_serve, 'before_server_start')
    app.register_listener(setup_serve, 'after_server_start')
    app.register_listener(teardown_serve, 'before_server_stop')


__all__ = [
    'register_listeners',
]

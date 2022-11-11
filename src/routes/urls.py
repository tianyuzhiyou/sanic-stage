# -*- coding: utf-8 -*-

"""项目所有的url蓝图定义"""

from apps.ping import (
    PingView,
    PingMysqlView,
    PingRedisView,
)
from apps.api import examples


def register_routes(app):
    # 基本url
    app.add_route(PingView.as_view(), '/')
    app.add_route(PingView.as_view(), '/ping')
    app.add_route(PingRedisView.as_view(), '/ping_redis')
    app.add_route(PingMysqlView.as_view(), '/ping_mysql')

    # 业务url
    app.add_route(examples.TestGetView.as_view(), "/test_get")
    app.add_route(examples.TestPostView.as_view(), "/test_post")


__all__ = ["register_routes"]

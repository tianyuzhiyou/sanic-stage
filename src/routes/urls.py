# -*- coding: utf-8 -*-

"""项目所有的url蓝图定义"""

from apps.ping import (
    PingView,
    LoggerView,
    PingMysqlView,
    PingRedisView,
    SentryView,
    PingCeleryView,
)


def register_routes(app):
    # 基本url
    app.add_route(PingView.as_view(), '/ping')
    app.add_route(SentryView.as_view(), "/ping_sentry")
    app.add_route(PingRedisView.as_view(), '/ping_redis')
    app.add_route(PingMysqlView.as_view(), '/ping_mysql')
    app.add_route(LoggerView.as_view(), '/logger')
    app.add_route(PingCeleryView.as_view(), "/ping_celery")


__all__ = ["register_routes"]

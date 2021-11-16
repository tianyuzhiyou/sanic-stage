# -*- coding: utf-8 -*-

__all__ = ["create_app"]

import logging
from sanic import Sanic

from config import config
from kits.error_handler import customer_exception_handler
from kits.listener import register_listeners
from kits.middleware import register_middlewares
from kits.serve_delay_task import register_delay_tasks
from routes.urls import register_routes
from kits.sentry_init import init_sentry
from utils.loggers import logger


def create_app(name: str = ""):
    """app工厂函数"""
    name = name if name else config.PROJECT_NAME
    # 创建app并加载初始配置
    app = Sanic(name, strict_slashes=True)
    app.config.update(config)
    logging.config.dictConfig(config.DEFAULT_LOG_CONFIG)  # 加载日志配置

    app.env_mode = app.config.ENV_MODE  # 获取环境变量
    app.debug = app.config.get("DEBUG", False)
    app.error_handler.add(Exception, customer_exception_handler)  # 加载异常处理器

    logger.info("当前是{}环境, debug是否开启：{}".format(app.config.ENV_MODE, app.debug))

    init_sentry(app)
    register_listeners(app)  # 注册钩子
    register_middlewares(app)  # 加载中间件
    register_routes(app)  # 注册路由
    register_delay_tasks(app)  # 加载异步协程任务动态更新配置

    return app

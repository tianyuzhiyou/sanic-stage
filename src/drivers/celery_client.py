# -*- coding: utf-8 -*-
import logging
from celery import Celery
from sentry_sdk.integrations.celery import CeleryIntegration
from celery.signals import worker_shutting_down, celeryd_init

from kits.sentry_init import init_sentry
from drivers.redis import redis_db
from drivers.mysql import db
from drivers.http_client import init_http_for_celery, close_http_for_celery
from utils.loggers import celery_logger
from config import config, celery_config
import celery_pool_asyncio  # 打补丁，支持async


class CeleryService(object):

    def get_celery_app(self):
        """获取celery对象"""
        celery_app = Celery(f'{config.PROJECT_NAME}-tasks',
                            broker=celery_config.CELERY_CONFIG["CELERY_BROKER_URL"],
                            include=celery_config.CELERY_TASKS
                            )
        celery_app.config = config  # 加载新属性，用于传递配置
        # 为celery对象更新配置
        celery_app.conf.update(
            accept_content=["json"],
            task_serializer="json",
            result_serializer="json"
        )
        celery_app.conf.update(celery_config.CELERY_CONFIG)  # 基础配置
        celery_app.conf.update(**config.get("CELERY_CONFIG", {}))  # 动态配置

        # sentry
        init_sentry(celery_app, CeleryIntegration)
        return celery_app


@celeryd_init.connect
async def init_celery(sender=None, conf=None, instance=None, **kwargs):
    # 直接输出到控制台,此时logger还无法打印
    logging.config.dictConfig(config.DEFAULT_LOG_CONFIG)
    celery_logger.info("celery worker启动，sender:{}".format(sender))
    if conf:
        class CeleryApp(object):
            pass

        local_app = CeleryApp()
        local_app.config = config

        celery_logger.info("celery worker启动，初始化redis,mysql...")
        await redis_db.init_redis_for_celery(local_app)
        await init_http_for_celery()
        await db.init_db(app=local_app)
        celery_logger.info("celery worker启动，初始化redis,mysql成功！")


@worker_shutting_down.connect
async def close(sender=None, **kwargs):
    """celery停止后发送信号关闭redis连接"""
    celery_logger.info("celery worker停止，关闭redis，mysql连接..., sender:{}, kwargs:{}".format(sender, kwargs))
    await redis_db.close_redis_cache()
    await close_http_for_celery()
    await db.close_db()
    celery_logger.info("celery worker停止，关闭redis，mysql连接成功！")

# -*- coding: utf-8 -*-
import logging
import functools
from utils.loggers import logger
from contextlib import asynccontextmanager
from config import config


def report_decorator(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        import time
        t1 = time.time()
        name, env, version = config.get("PROJECT_NAME"), config.get("ENV_MODE"), config.get("CURRENT_VERSION")
        logger.info("{}-{}环境-{}版本开始执行脚本...".format(name, env, version))
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            logger.error("{}环境-{}版本执行出错:{}".format(env, version, e))
        else:
            logger.info("当前进度:100%......")
            logger.info("{}环境-{}版本脚本执行成功，耗时:{}".format(env, version, time.time() - t1))
            return res

    return new_func


@asynccontextmanager
async def init_app():
    """
    @desc 加载配置
    :param app:
    :param loop:
    :return:
    """
    from drivers.redis import redis_db
    from drivers.mysql import db
    from drivers.http_client import init_http_for_celery, close_http_for_celery
    try:
        logging.config.dictConfig(config.DEFAULT_LOG_CONFIG)

        class InitApp(object):
            pass

        local_app = InitApp()
        local_app.config = config
        logger.info("加载环境中....")
        await init_http_for_celery()
        await redis_db.init_redis_for_celery(local_app)
        await db.init_db(local_app)
        logger.info("环境加载完毕....")
        yield
    finally:
        await close_http_for_celery()
        await redis_db.close_redis_cache()
        await db.close_db()
        logger.info("任务完成，清理环境完成.....")

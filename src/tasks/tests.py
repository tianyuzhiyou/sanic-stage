# -*- coding: utf-8 -*-

"""测试celery连接用"""

from utils.loggers import celery_logger
from celery_worker import celery_app
from business import biz


@celery_app.task
async def celery_test():
    celery_logger.info("celery 任务接收成功！")
    await biz.ping.ping()
    celery_logger.info("celery 任务执行成功！")
    return "OK"

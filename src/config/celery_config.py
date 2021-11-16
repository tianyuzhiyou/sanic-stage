# -*- coding: utf-8 -*-

"""celery的配置"""

from kombu import Queue
from config import basic
from celery.schedules import crontab, timedelta

# 注册task任务模块
CELERY_TASKS = [
    "tasks.tests",
]

# 定义队列、路由和交换机
TASK_QUEUES = (
    Queue(
        "sanic-stage.default",
        routing_key="sanic-stage.default"),
)

# celery的配置
CELERY_CONFIG = {
    "CELERY_BROKER_URL": "amqp://admin:admin@0.0.0.0:5672/",  # 设置celery的发送地址
    "CELERY_QUEUES": TASK_QUEUES,
    "CELERY_DEFAULT_QUEUE": basic.PROJECT_NAME + ".default",
    "CELERY_DEFAULT_EXCHANGE_TYPE": "direct",
    "CELERY_DEFAULT_ROUTING_KEY": basic.PROJECT_NAME + ".default",
    # 设置序列化方式
    "CELERY_TASK_SERIALIZER": 'json',
    "CELERY_RESULT_SERIALIZER": 'json',
    "CELERY_ACCEPT_CONTENT": ["json"],
    "CELERY_TIMEZONE": 'Asia/Shanghai',
    "CELERY_ENABLE_UTC": True,
    "CELERY_IGNORE_RESULT": True,
    "CELERYD_POOL_RESTARTS": True,
    # 定义具体的任务绑定队列
    "CELERY_ROUTES": {
        "tasks.tests.celery_test": {
            "queue": "sanic-stage.default",
        },
    },
    # celery beat
    "CELERYBEAT_SCHEDULE": {
        # "key": {
        #     'task': 'tasks.tests.celery_test',
        #     'schedule': timedelta(minutes=1),  # 每分钟一次
        #     'args': ()
        # },
    }
}

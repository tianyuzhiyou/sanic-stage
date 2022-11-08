# -*- coding: utf-8 -*-

import os
import sys
from distutils.util import strtobool

# Basic config
PROJECT_NAME = 'sanic-stage'  # 定义项目名称
CURRENT_VERSION = '1.0.0'  # 当前版本
ENV_MODE = os.getenv('ENV_MODE', 'local')  # 当前环境
DEBUG = strtobool(str(os.getenv("DEBUG", True)))  # 是否开启DEBUG模式
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')  # 日志等级

ADD_REQUEST_LOG = False  # 是否开启http请求日志详细打印，默认false
# 需要排除不打印日志的url
EXCLUDE_LOG_URL_MAP = {}

# http的socket连接个数上限
HTTP_REQUEST_CONCURRENCY_LIMIT = 100
# default http request timeout
REQUEST_TIMEOUT = 60

# 根目录
PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

# consul配置信息
CONFIG_FROM_CONSUL = False  # 配置是否从consul拉取配置
# consul连接配置, CONFIG_FROM_CONSUL 为True时才使用
CONSUL_HOSTS = {
    # 'pd': {'host': '127.0.0.1', 'port': 9900},
}

# sentry config
SENTRY_DSN = ""

# mysql config
ENABLE_DB = False # 是否启用mysql
MYSQL_CONFIG = {
    # "default": {
    # "host": "127.0.0.1",
    # "port": 3306,
    # "db": "test",
    # "user": "root",
    # "password": "123456",
    # "pool_min_size": 5,
    # "pool_max_size": 20,
    # "autocommit": True,
    # },
}

# redis config
ENABLE_REDIS = False # 是否启用redis
REDIS_CONFIG = {
    # "default": {
    # "address": "redis://:127.0.0.1:6379/0",
    # "timeout": 10,
    # "minsize": 3,
    # "maxsize": 50,
    # "encoding": "utf-8",
    # }
}

# upstream services
ENDPOINTS = {
    # "baidu": "https://www.baidu.com/"
}

# Basic Log config
DEFAULT_LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "app": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": True,
            "qualname": "default",
        },
        "access": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": True,
            "qualname": "default",
        },
        "http": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": True,
            "qualname": "default",
        },
        "celery": {
            "level": LOG_LEVEL,
            "handlers": ["console"],
            "propagate": True,
            "qualname": "default",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
    },
    "formatters": {
        "generic": {
            # 时间，函数位置, 日志等级，详细信息
            "format": "[%(asctime)s] [%(name)s.%(module)s.%(funcName)s:%(lineno)s] %(levelname)s: %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S]",
            "class": "logging.Formatter",
        },
    },
}

# -*- coding: utf-8 -*-
import os

# Basic Serve config
# 本地服务的ip
SERVE_HOST = "0.0.0.0"
# 本地服务的端口
SERVE_PORT = 9000
# 是否打印access日志
SERVE_ACCESS_LOG = True
# woker数量
SERVE_WORKERS = 3
# 单个请求大小上线
SERVE_REQUEST_MAX_SIZE = 100 * 1024 * 1024
# 单个请求超时时间
SERVE_REQUEST_TIMEOUT = 3

# 本地测试时
MYSQL_CONFIG = {
    "default": {
        "host": "0.0.0.0",
        "port": 3306,
        "db": "test",
        "user": "root",
        "password": "123456",
        "pool_min_size": 5,
        "pool_max_size": 20,
        "autocommit": True,
    },
}

# redis配置

REDIS_CONFIG = {
    "default": {
        "address": "redis://127.0.0.1:6379/0",
        "timeout": 10,
        "minsize": 3,
        "maxsize": 50,
        "encoding": "utf-8",
    }
}
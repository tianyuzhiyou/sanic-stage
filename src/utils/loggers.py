# -*- coding:utf-8 -*-

import logging

logger = logging.getLogger("app") # 业务主动打印
access_logger = logging.getLogger("access") # 中间价打印
http_logger = logging.getLogger("http") # 服务层日志使用
celery_logger = logging.getLogger("celery") # celery日志使用
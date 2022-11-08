# -*- coding: utf-8 -*-
"""
启动命令： celery -A worker:celery_app worker --concurrency=3 -P celery_pool_asyncio:TaskPool
"""

from services import svc

celery_app = svc.celery_app

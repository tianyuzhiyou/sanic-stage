# -*- coding: utf-8 -*-

__all__ = ["svc"]

from services.ping import PingService
from drivers.celery_client import CeleryService
from .examples.service import ExampleService

class Service(object):
    """服务层"""
    ping = PingService()
    celery_app = CeleryService().get_celery_app()
    example_svc = ExampleService()

svc = Service()

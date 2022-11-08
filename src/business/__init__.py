# -*- coding: utf-8 -*-

"""
业务逻辑层，用来封装聚合业务逻辑
"""

__all__ = ["biz"]

from business.ping import PingBusiness
from .examples.business import ExampleBusiness


class Business(object):
    """业务层"""
    ping = PingBusiness()
    example = ExampleBusiness()


biz = Business()

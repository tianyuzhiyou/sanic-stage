# -*- coding: utf-8 -*-

__all__ = ["biz"]

from business.ping import PingBusiness


class Business(object):
    """业务层"""
    ping = PingBusiness()


biz = Business()

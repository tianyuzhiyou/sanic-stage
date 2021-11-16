# -*- coding: utf-8 -*-

from sentry_sdk import capture_exception
from sentry_sdk import capture_message


def sentry_exception(e):
    """上报 Sentry 错误信息"""
    capture_exception(e)


def sentry_message(msg):
    """上报 Sentry 日志消息"""
    capture_message(msg)

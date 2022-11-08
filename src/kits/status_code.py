# -*- coding: utf-8 -*-
"""
定义全局错误码
"""

from enum import Enum, unique


@unique
class Code(Enum):
    FEEDBACK = (400, '')
    SUCCESS = (200, 'success')
    UNAUTHORIZED = (401, '身份认证信息未提供。')
    FORBIDDEN = (403, '无权限')
    NOT_FOUND = (404, '无法找到页面')
    METHODNOTSUPPORT = (405, "请求方式不允许")
    SYSTEM_ERROR = (500, '服务器开小差了，请稍后重试~')
    PARAM_MISS = (400, '参数缺失！')
    PARAM_ERROR = (400, '参数错误！')

    # other
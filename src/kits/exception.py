# -*- coding: utf-8 -*-

"""
定义标准异常抛出
所有的错误类继承基础类
"""
from .status_code import Code


class Error(Exception):
    """异常错误基础类"""
    msg = None
    code = None
    status_code = 500

    def __init__(self, code_enum: Code, msg: str = None, status_code=None):
        _code, _msg = code_enum.value
        self.code = _code
        if status_code is not None:
            self.status_code = status_code
        self.msg = msg if msg else _msg

    def __str__(self):
        return f"{self.__class__.__name__}: {self.code}, {self.msg}"


class FeedBackException(Error):
    """错误反馈提示，用于给前端的提示"""
    status_code = 200

    def __init__(self, code_enum: Code = Code.FEEDBACK, msg: str = "", status_code=None):
        super().__init__(code_enum=code_enum, msg=msg, status_code=status_code)


class ParamsException(Error):
    """错误反馈提示,用于参数校验错误返回"""
    status_code = 200

    def __init__(self, code_enum: Code = Code.PARAM_ERROR, msg: str = "", status_code=None):
        super().__init__(code_enum=code_enum, msg=msg, status_code=status_code)


class MethodNotSupportException(Error):
    """方法不允许"""
    status_code = 405

    def __init__(self, code_enum: Code = Code.METHODNOTSUPPORT, msg: str = "", status_code=None):
        super().__init__(code_enum=code_enum, msg=msg, status_code=status_code)


class ServiceException(Error):
    """用于服务器内部错误"""
    status_code = 500  # 此时返回500，致命错误

    def __init__(self, code_enum: Code = Code.SYSTEM_ERROR, msg: str = "", status_code=None):
        super().__init__(code_enum=code_enum, msg=msg, status_code=status_code)


class UpstreamException(Error):
    """用于调用其他内部接口发生报错"""
    status_code = 500

    def __init__(self, code_enum: Code = Code.SYSTEM_ERROR, msg: str = "", status_code=None):
        super().__init__(code_enum=code_enum, msg=msg, status_code=status_code)


__all__ = [
    "ServiceException",
    "FeedBackException",
    "UpstreamException",
    "ParamsException",
    "MethodNotSupportException",
    "Error"
]

# -*- coding: utf-8 -*-
import traceback

from sanic import response
from sanic.exceptions import MethodNotSupported, NotFound

from kits.status_code import Code
from .exception import Error
from utils.loggers import access_logger


def customer_exception_handler(request, exception):
    if isinstance(exception, Error):
        data = {
            'result': False,
            'resultcode': exception.code,
            'msg': '',
            'errormsg': str(exception.msg),
            'data': {},
            'resultfrom': request.app.config.PROJECT_NAME,
        }
        return response.json(data, status=exception.status_code)
    elif isinstance(exception, (NotFound, MethodNotSupported)):
        # 路由不存在
        errormsg = str(exception)
        exc_data = None

        data = {
            'result': False,
            'errormsg': errormsg,
            'resultcode': exception.status_code,
            'data': exc_data,
            'resultfrom': request.app.config.PROJECT_NAME,
        }
        return response.json(data, status=exception.status_code)
    else:
        code, errormsg = Code.SYSTEM_ERROR.value
        exc_data = None

        # 出现服务器错误，记录错误日志
        if request.app.config.get("ADD_REQUEST", False):
            access_logger.error(f"url: {request.path}, method: {request.method},err:{str(exception)}", exc_info=True)

        if request and request.app.config.DEBUG:
            errormsg = errormsg + ', err: {}'.format(str(exception))
            traceback.print_exc()
            exc_data = traceback.format_exc()

        data = {
            'result': False,
            'errormsg': errormsg,
            'resultcode': code,
            'data': exc_data,
            'resultfrom': request.app.config.PROJECT_NAME,
        }
        return response.json(data, status=code)


__all__ = [
    'customer_exception_handler'
]

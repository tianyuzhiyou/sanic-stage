# -*- coding: utf-8 -*-
import time
import aiotask_context as context
from sanic import Sanic
from sanic.response import HTTPResponse
from sanic.request import Request

from utils.json_tool import json_dumps, json_loads
from kits.status_code import Code
from utils.loggers import access_logger
from kits.exception import MethodNotSupportException


async def request_hijack_middleware(request):
    access_methods = ('GET', "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE", "CONNECT")
    if request.method not in access_methods:
        raise MethodNotSupportException()


async def init_app_context(request):
    context.set('app', request.app)
    context.set('accesstoken', request.headers.get('accesstoken', ''))
    context.set('x-platform', str(request.headers.get('x-platform', '')).upper())


# 请求中间件
async def request_middleware(request):
    await init_app_context(request)  # 添加上下文
    request.ctx.run_time = time.time()
    await request_hijack_middleware(request)


async def bare_dict_as_http_response(request, response):
    if not isinstance(response, HTTPResponse):
        body = {
            'result': True,
            'resultcode': Code.SUCCESS.code,
            'msg': '',
            'errormsg': '',
            'data': response,
            'resultfrom': request.app.config.PROJECT_NAME,
        }
        response = HTTPResponse(
            json_dumps(body),
            headers=None,
            content_type="application/json; charset=utf-8",
            status=200,
        )

    if request.app.config.get("ADD_REQUEST_LOG", False):
        request.app.add_task(add_request_log(request, response))

    return response


async def add_request_log(request: Request, response: HTTPResponse):
    """添加请求日志"""
    if request.path in request.app.config.get("EXCLUDE_LOG_URL_MAP", {}):
        return

    # add run_time
    try:
        request.ctx.run_time
    except Exception:
        return
    duration = time.time() - request.ctx.run_time
    response.headers["elapsed_time"] = duration
    http_extra = {
        "duration": duration,
        "method": request.method,
        "ip": request.ip
    }

    # add request data
    if request.body:
        try:
            http_extra['body'] = json_loads(request.body.decode("utf-8"))
        except Exception:
            http_extra['body'] = request.body
    if request.query_args:
        http_extra['params'] = dict(request.query_args)

    # add os msg
    for header in ['referer', 'os', 'prad']:
        val = request.headers.get(header, None)
        if val:
            http_extra[header] = val

    # add response body
    if request.app.config.get("DEBUG", False) and response.body:
        # 开启debug模式时，打印返回结果
        try:
            resp_json = json_loads(response.body.decode("utf-8"))
            http_extra['result'] = str(resp_json)[:2000]
        except Exception:
            http_extra['result'] = response.body[:2000]

    access_logger.info("access url: {} msg: {}".format(request.path, http_extra))


# 响应中间件
async def response_middleware(request: Request, response: HTTPResponse):
    response = await bare_dict_as_http_response(request, response)
    return response


def register_middlewares(app: Sanic):
    app.register_middleware(request_middleware, 'request')
    app.register_middleware(bare_dict_as_http_response, 'response')


__all__ = [
    'register_middlewares',
]

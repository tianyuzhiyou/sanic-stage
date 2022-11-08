# -*- coding: utf-8 -*-

"""
请求网关校验处理
"""
import functools
from kits.status_code import Code


def authenticate_user(*args):
    def decorator(f):
        @functools.wraps(f)
        async def decorated_function(request, *f_args, **f_kwargs):
            # 从网关获取获取透传信息赋值给request
            is_authorized = True
            if is_authorized:
                response = await f(request, *f_args, **f_kwargs)
                return response
            else:
                raise Code.UNAUTHORIZED

        return decorated_function

    if args:
        return decorator(*args)
    else:
        return decorator

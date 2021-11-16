# -*- coding: utf-8 -*-
"""
http://www.ruanyifeng.com/blog/2016/04/cors.html
非简单请求的CORS请求，会在正式通信之前，增加一次HTTP查询请求，称为"预检"请求（preflight）
"预检"请求用的请求方法是OPTIONS
"""
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView


class EEBOMethodView(HTTPMethodView):
    async def options(self, request):
        return HTTPResponse(status=200)

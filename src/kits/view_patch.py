# -*- coding: utf-8 -*-
"""
非简单请求的CORS请求，会在正式通信之前，增加一次HTTP查询请求，称为"预检"请求（preflight）
"预检"请求用的请求方法是OPTIONS
"""
from sanic.response import HTTPResponse
from sanic.views import HTTPMethodView


class CorsMethodView(HTTPMethodView):
    async def options(self, request):
        return HTTPResponse(status=200)

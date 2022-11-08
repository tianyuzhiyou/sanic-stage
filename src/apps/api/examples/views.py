# -*- coding: utf-8 -*-

"""
api示例
"""

__all__ = [
    "TestGetView", "TestPostView"
]

from kits.auth import authenticate_user
from kits.exception import ParamsException
from kits.view_patch import CorsMethodView

from utils.base_validations import DataValidator
from . import validations as val
from business import biz


class TestGetView(CorsMethodView):
    decorators = [authenticate_user]

    async def get(self, request):
        """
        @desc GET请求示例
        :param request:
        :return:
        """
        val_obj = DataValidator(val.ExampleValidator, dict(request.query_args) if request.query_args else {})
        if not val_obj.is_valid():
            raise ParamsException(msg=val_obj.errors["errmsg"][0])
        # dosomthing
        result = await biz.example.biz_test_get(val_obj.validate_data)
        return result


class TestPostView(CorsMethodView):
    decorators = [authenticate_user]

    async def post(self, request):
        """
        @desc POST请求示例
        :param request:
        :return:
        """
        val_obj = DataValidator(val.ExampleValidator, dict(request.query_args) if request.query_args else {})
        if not val_obj.is_valid():
            raise ParamsException(msg=val_obj.errors["errmsg"][0])
        # dosomthing
        result = await biz.example.biz_test_post(val_obj.validate_data)
        return result

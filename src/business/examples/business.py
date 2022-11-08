# -*- coding: utf-8 -*-
from services import svc


class ExampleBusiness(object):

    async def biz_test_get(self, params) -> dict:
        """
        @desc 处理TestGetView 逻辑
        :param params:
        :return:
        """
        # do something
        data = await svc.example_svc.ser_test_get(params)
        return data

    async def biz_test_post(self, params) -> dict:
        """
        @desc 处理TestPostView 逻辑
        :param params:
        :return:
        """
        # do something
        data = await svc.example_svc.ser_test_post(params)
        return data

# -*- coding: utf-8 -*-

import pytest
from scripts.tools import init_app
from utils.cache import RedisProxy

"""
pytest 单元测试示例
"""


@pytest.fixture(scope="class", autouse=True)
def class_scope():
    print("每个类执行一次")


@pytest.fixture(scope="function", name="function")
def function_scope():
    print("每个用例执行前执行一次")
    yield
    print("每个用例执行后执行一次")


@pytest.fixture(scope="function", name="function2")
def function_scope2():
    print("function_scope2: 每个用例执行前执行一次")
    yield "scope2"
    print("function_scope2: 每个用例执行后执行一次")


class TestView:

    @pytest.mark.asyncio
    async def test_one(self):
        async with init_app():
            cache = RedisProxy()
            await cache.set("aaaa", "1111")
            res = await cache.get("aaaa")
            print(res)

    @pytest.mark.usefixtures("function")
    def test_two(self):
        print("test_1........")
        assert True

    def test_three(self, function2):
        print("test_2:{}".format(function2))

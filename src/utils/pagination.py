# -*- coding: utf-8 -*-
"""
分页工具
"""

from collections import OrderedDict


class Pagination(object):
    max_limit = 100

    def __init__(self, p: int = 1, limit: int = 10):
        self.limit = self.__get_limit(limit)
        self.page = self.__get_page(p)
        self.total_page = None
        self.total_count = 0

    def __get_limit(self, limit: int) -> int:
        """
        获取请求中，每页多少行
        """
        return limit if limit < self.max_limit else self.max_limit

    def __get_page(self, page: int) -> int:
        """
        获取请求中，当前第几页
        """
        return page if page > 0 else 1

    def get_offset(self) -> int:
        """
        获取请求中，当前开始行的下标(一般用页码，而不使用这个值)
        """
        return (self.page - 1) * self.limit

    def get_total_page(self, total_count: int):
        """
        @desc 获取总页数
        :param total_count:
        :return:
        """
        self.total_page = total_count // self.limit if total_count % self.limit == 0 else total_count // self.limit + 1
        self.total_count = total_count
        return self.total_page

    async def get_paginated_response(self, data: list) -> dict:
        """
        分页条返回内容
        :param data:
        :return:
        """
        return OrderedDict([
            ('p', self.page),
            ('limit', self.limit),
            ('offset', self.get_offset()),
            ('totalpage', self.total_page),
            ('total_count', self.total_count),
            ('objects', data)
        ])

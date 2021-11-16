# -*- coding: utf-8 -*-
"""
简单分页工具
"""


def get_paging_parameter(parameter_dict: dict):
    p = int(parameter_dict.pop('p', 1))
    limit = int(parameter_dict.pop('limit', 10))
    offset = parameter_dict.pop('offset', None)

    if p < 1:
        p = 1
    if limit < 1:
        limit = 1
    elif limit > 1000:
        limit = 1000
    if offset:
        offset = int(offset) if int(offset) >= 0 else 0
    else:
        offset = (p - 1) * limit
    return parameter_dict, p, limit, offset


def get_totalpage(total_count: int, limit: int):
    return total_count // limit if total_count % limit == 0 else total_count // limit + 1


def get_offset(p: int, limit: int):
    return (p - 1) * limit

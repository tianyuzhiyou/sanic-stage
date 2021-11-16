# -*- coding: utf-8 -*-

import orjson
import datetime

__all__ = ['default', 'json_dumps', 'json_loads']


def default(obj):
    if isinstance(obj, datetime.datetime):
        return int(obj.timestamp() * 1000)
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    raise TypeError


def json_dumps(data):
    res = orjson.dumps(data, default=default, option=orjson.OPT_PASSTHROUGH_DATETIME)
    return res


def json_loads(data):
    return orjson.loads(data)

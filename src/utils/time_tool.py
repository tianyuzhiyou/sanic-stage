# -*- coding: utf-8 -*-

import time
from datetime import datetime as dt, date as d
from typing import Union


class TimeTool(object):

    NULL_STR_DATE = "1970-01-01"
    DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S"  # 默认时间格式
    DEFAULT_DATE_FORMAT = "%Y-%m-%d"  # 默认日期格式
    DEFAULT_MONTH_FORMAT = "%Y-%m"  # 默认月份格式

    CONFIG = {
        "format_str": DEFAULT_FORMAT,  # {string} 时间格式化的格式字符串
        "format_list": (
            DEFAULT_FORMAT, "%Y-%m-%d %H:%M:%S.%f", DEFAULT_DATE_FORMAT, "%Y年%m月%d日 %H时%M分%S秒",
            "%Y年%m月%d日　%H时%M分%S秒", "%Y年%m月%d日 %H时%M分", "%Y年%m月%d日　%H时%M分", "%Y年%m月%d日 %H:%M:%S",
            "%Y年%m月%d日　%H:%M:%S", "%Y年%m月%d日 %H:%M", "%Y年%m月%d日　%H:%M", "%Y年%m月%d日",
            "%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M:%S.%f", "%Y/%m/%d", "%Y%m%d", "%Y%m%d%H%M%S",
            "%Y/%m/%d %H:%M", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S+08:00", "%Y-%m-%dT%H:%M:%S.%f+08:00",
        )
    }

    @staticmethod
    def str_date_to_timestamp(value: str, formal: str = "%Y-%m-%d %H:%M:%S") -> int:
        """时间字符串转换时间戳"""
        return int(time.mktime(time.strptime(value, formal)))

    @staticmethod
    def date_to_string(date_time: Union[dt, d], format_str: str = "%Y-%m-%d"):
        """时间转换时间字符串"""
        if isinstance(date_time, (dt, d)):
            return date_time.strftime(format_str)
        raise ValueError(f"参数{date_time}: 时间-->时间字符串失败")

    @staticmethod
    def date_now() -> dt:
        """当前时间"""
        return dt.now()

    @staticmethod
    def date_today() -> d:
        """当前日期"""
        return d.today()

    @classmethod
    def str_date_now(cls) -> str:
        """当前时间字符串"""
        return cls.date_to_string(cls.date_now())

    @classmethod
    def str_date_today(cls) -> str:
        """当前日期字符串"""
        return cls.date_to_string(cls.date_today())

    @classmethod
    def timestamp_to_string(cls, timestamp: int, format_str: str = "%Y-%m-%d"):
        """时间戳住转换时间字符串"""
        if isinstance(timestamp, int):
            timestamp = timestamp / 1000
            date_time = dt.utcfromtimestamp(timestamp)
            return cls.date_to_string(date_time, format_str)
        raise ValueError(f"参数{timestamp}: 时间戳-->时间字符串失败")

    @classmethod
    def string_to_date(cls, date_str: str, format_str: str = "%Y-%m-%d"):
        """时间字符串转换时间"""
        if isinstance(date_str, str):
            if format_str:
                try:
                    _time = dt.strptime(date_str, format_str)
                    return d(_time.year, _time.month, _time.day)
                except Exception:
                    pass
            for fm in cls.CONFIG.get("format_list"):
                try:
                    _time = dt.strptime(date_str, fm)
                    return d(_time.year, _time.month, _time.day)
                except:
                    pass
        raise ValueError(f"参数{date_str}: 时间字符串-->时间失败")


time_tool = TimeTool()

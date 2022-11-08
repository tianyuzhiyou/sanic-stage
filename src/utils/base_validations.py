# -*- coding: utf-8 -*-

__all__ = ["DataValidator",
           "LengthValidator",
           "BlankValidator",
           "ValidatorManager",
           "UUIDStrValidator",
           "ChoiceValidator"]

import re
import uuid
from typing import Any, List

from pydantic import ValidationError

from .json_tool import json_loads


class DataValidator(object):
    def __init__(self, validator, data: dict, is_update: bool = False):
        """
        @desc　基础校验器
        :param validator:
        :param data:
        """
        self._class_validator = validator
        self._validator = None
        self.data = data
        self.validate_data = None
        self.is_update = is_update
        self.errors = {}

    def is_valid(self):
        """
        @desc　验证数据
        :return:
        """
        try:
            self._validator = self._class_validator(**self.data)
        except ValidationError as e:
            errmsg = [i["msg"] if ":" in i["msg"] else "{}:{}".format(i["loc"][0], i["msg"]) for i in
                      json_loads(e.json())]
            self.errors = {"code": 10101, "errmsg": errmsg}
            return False
        else:
            data = self._validator.dict()
            if self.is_update:
                # 在更新时以self.data为准，防止默认生成的数据造成不可知的影响
                data = {k: v for k, v in data.items() if k in self.data}
            self.validate_data = data
            return True


class BaseValidator(object):
    def is_valid(self, value, label: str = None):
        raise ValueError("必须重写该方法")

    @staticmethod
    def label_str(value: str) -> str:
        return "{}:".format(value) if value else ""


class ValidatorManager(object):
    @classmethod
    def is_valid(cls, value, val_tors: List[BaseValidator], label: str = None):
        """
        @desc　验证所有的选择
        :param value:
        :return:
        """
        for val in val_tors:
            value = val.is_valid(value, label)
        return value


class LengthValidator(BaseValidator):
    def __init__(self, max_length: int = None, min_length: int = None):
        self._max_length = max_length
        self._min_length = min_length

    def is_valid(self, value, label: str = None) -> Any:
        le = len(value)
        if (self._max_length is not None and le > self._max_length):
            raise ValueError("{}长度必须小于{}".format(self.label_str(label), self._max_length))
        elif (self._min_length is not None and le < self._min_length):
            raise ValueError("{}长度必须大于{}".format(self.label_str(label), self._min_length))
        return value


class BlankValidator(BaseValidator):
    def __init__(self, blank: bool = True, null: bool = True):
        self._blank = blank
        self._null = null

    def is_valid(self, value, label: str = None) -> Any:
        if not self._blank and value == "":
            raise ValueError("{}不允许为空字符串".format(self.label_str(label)))
        if not self._null and value is None:
            raise ValueError("{}不允许为None".format(self.label_str(label)))
        return value


class NameStrValidator(BaseValidator):
    def __init__(self, allow_emoji: bool = False, need_null_chat: bool = False):
        """
        @desc 该校验器用于严格名字场景，只允许字母、数字、汉字、-，_
        :param allow_emoji: 是否允许任何字符
        :param need_null_chat: 是否去除空格
        """
        self._allow_emoji = allow_emoji
        self.need_null_chat = need_null_chat

    def is_valid(self, value, label: str = None) -> Any:
        if not value:
            return value
        if self.need_null_chat:
            value = str(value).replace(" ", "")
        if not re.search(r'^[-_a-zA-Z0-9\u4e00-\u9fa5]+$', value):
            raise ValueError("{}存在非法字符".format(self.label_str(label)))
        return value


# 用于去除非法字符
class CleanEmojiValidator(BaseValidator):

    def is_valid(self, value, label: str = None) -> Any:
        if not value:
            return value
        pattern = r'[0-9a-zA-Z#<《》>/、\\。\.，,\？?；;：:!！@\$￥%\^&\*\(（）\)_\-\+=\[\]`~{}\u4E00-\u9FA5]+'
        c = re.findall(pattern, value)
        if c:
            return "".join(c)
        return ""


# uuid校验
class UUIDStrValidator(BaseValidator):
    def __init__(self, allow_null: bool = True, allow_blank: bool = True):
        self._allow_null = allow_null
        self._allow_blank = allow_blank

    def is_valid(self, value, label: str = None) -> Any:
        if not self._allow_blank and value == "":
            raise ValueError("{}不允许为空字符串".format(self.label_str(label)))
        if not self._allow_null and value is None:
            raise ValueError("{}不允许为None".format(self.label_str(label)))
        if value in ("", None):
            return value
        try:
            value = uuid.UUID(value).hex
        except Exception:
            raise ValueError("{}不符合UUID格式".format(self.label_str(label)))
        else:
            return value


# 枚举校验
class ChoiceValidator(BaseValidator):
    def __init__(self, choices: list):
        self._choices = set(choices)

    def is_valid(self, value, label: str = None) -> Any:
        if value not in self._choices:
            raise ValueError("{}请在{}中选择".format(self.label_str(label), self._choices))
        return value


# 空格校验
class StripValidator(BaseValidator):
    def __init__(self, middle: bool = False, l_r: bool = True, return_str: bool = False):
        self._middle = middle
        self.l_r = l_r
        self._return_str = return_str

    def is_valid(self, value, label: str = None) -> Any:
        if not value:
            return "" if self._return_str else value
        if self.l_r:
            value = str(value).strip()
        if self._middle:
            value = str(value).replace(" ", "")
        return value


# 整数校验
class DigitValidator(BaseValidator):
    def __init__(self, blank: bool = True, null: bool = True):
        self._blank = blank
        self._null = null

    def is_valid(self, value, label: str = None) -> int:
        if not self._blank and value == "":
            raise ValueError("{}不允许为空字符串".format(self.label_str(label)))
        if not self._null and value is None:
            raise ValueError("{}不允许为None".format(self.label_str(label)))
        try:
            value = int(value)
        except Exception:
            raise ValueError("{}格式错误".format(self.label_str(label)))
        else:
            return value

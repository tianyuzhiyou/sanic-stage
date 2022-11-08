from typing import List
from pydantic import BaseModel
from pydantic import validator

from utils.base_validations import ValidatorManager, LengthValidator

"""
定义参数校验方法
"""

class ExampleValidator(BaseModel, ValidatorManager):
    test_str: str
    test_int: int
    test_list: List[str]

    @validator("test_list")
    def validate_test_list(cls, v: list):
        """
        针对每个参数做特殊校验，固定的写法
        """
        val_list = [LengthValidator(max_length=10, min_length=1)]
        for index, k in enumerate(v):
            v[index] = cls.is_valid(k, val_tors=val_list)
        return v
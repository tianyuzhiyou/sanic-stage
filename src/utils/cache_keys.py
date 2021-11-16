# -*- coding: utf-8 -*-

from config import config


def set_key(key: str) -> str:
    """
    @desc　设置缓存
    :param key:
    :return:
    """
    return "{}:{}".format(config.PROJECT_NAME, key)


class CommonKey(object):
    """
    公有缓存,没有自动前缀
    """
    pass

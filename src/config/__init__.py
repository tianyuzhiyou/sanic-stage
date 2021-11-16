# -*- coding: utf-8 -*-

from sanic.config import Config

from . import basic
from . import local_config

# 加载基础配置
config = Config()
config.update_config(basic)

# 加载本地动态配置
if config.ENV_MODE == "local":
    config.update_config(local_config)

# 远程加载consul配置
if config.CONFIG_FROM_CONSUL:
    from drivers.consul import DynamicConfigFromConsul

    init_consul_config = DynamicConfigFromConsul(
        **config.CONSUL_HOSTS[config.ENV_MODE],
        namespace=config.PROJECT_NAME,
        app_type='data',
    )
    # 拉取consul配置更新本地的basic配置
    init_consul_config.init_config(config)

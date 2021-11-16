# -*- coding: utf-8 -*-
from sanic import Sanic

from drivers.consul import DynamicConfigFromConsul


async def update_dynamic_config(app: Sanic):
    if app.config.CONFIG_FROM_CONSUL:
        consul_basic_config = app.config.CONSUL_HOSTS.get(app.config.ENV_MODE, {})
        consul_config = DynamicConfigFromConsul(**consul_basic_config, namespace=app.config.PROJECT_NAME, app_type="data")
        # 启动一个异步任务去获取consul的动态配置
        app.add_task(
            consul_config.update_config(app.config, app.loop)
        )


def register_delay_tasks(app: Sanic):
    app.add_task(update_dynamic_config(app))


__all__ = ['register_delay_tasks']

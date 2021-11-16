# -*- coding: utf-8 -*-

"""定义sentry初始化"""

import sentry_sdk
from sentry_sdk.integrations.sanic import SanicIntegration
from kits.exception import FeedBackException, ParamsException, MethodNotSupportException


def init_sentry(app, integration=SanicIntegration):
    if app.config.SENTRY_DSN:
        sentry_sdk.init(
            dsn=app.config.SENTRY_DSN,
            integrations=[integration()],
            send_default_pii=True,
            ignore_errors=[FeedBackException, ParamsException, MethodNotSupportException],
            environment=app.config.ENV_MODE,
            release=app.config.CURRENT_VERSION,
        )

# -*- coding: utf-8 -*-

"""web服务启动入口"""

import logging

from application import create_app
from utils.loggers import logger

app = create_app()

if __name__ == "__main__":
    import argparse

    if app.config.get('ENV_MODE') == 'local':
        logging.basicConfig(level=logging.DEBUG)
    logger.info(f'**************** 路由加载中 ****************')
    for router_key in app.router.routes_all:
        logger.info(router_key)
    logger.info(
        f'**************** 路由加载完成! 共{len(app.router.routes_all)}个路由 ****************')

    parser = argparse.ArgumentParser(description="run web-serve app.")
    parser.add_argument(
        "-a",
        "--host",
        type=str,
        default=app.config.SERVE_HOST,
        help="The host of server bind to.",
    )
    parser.add_argument(
        "-p", "--port", type=int, default=app.config.SERVE_PORT, help="The port of server bind to."
    )
    args = parser.parse_args()

    logger.info(f"*********** [ 当前配置环境 ENV_MODE: {app.config.ENV_MODE}] ***********")
    app.run(host=args.host,
            port=args.port,
            debug=app.config.get("DEBUG", True),
            access_log=app.config.get("SERVE_ACCESS_LOG", False),
            workers=app.config.get("SERVE_WORKERS", 1),
            auto_reload=app.config.get('AUTO_RELOAD', False),
            )

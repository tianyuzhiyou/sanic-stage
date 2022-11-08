# -*- coding: utf-8 -*-

"""脚本例子"""

import asyncio
import aiotask_context as context
from scripts.tools import report_decorator, init_app
from utils.loggers import logger


def test_task():
    async def _handler():
        async with init_app():
            # do something
            pass
            logger.debug("脚本任务执行成功...")

    loop = asyncio.get_event_loop()
    loop.set_task_factory(context.task_factory)
    loop.run_until_complete(_handler())


@report_decorator
def run():
    test_task()


if __name__ == "__main__":
    run()

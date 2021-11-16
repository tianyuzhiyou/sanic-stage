# -*- coding: utf-8 -*-
"""定义脚本命令"""

from invoke import task

from config import config


@task
def start_worker(c):
    c.run('celery -A celery_worker:celery_app worker --concurrency=2 -P celery_pool_asyncio:TaskPool --scheduler celery_pool_asyncio:PersistentScheduler --loglevel DEBUG')


@task
def run_scripts_long(c):
    """构建长脚本命令,
    执行命令：inv -c scripts_worker run-scripts-long
    """
    version: str = config.get('CURRENT_VERSION')
    file_name = f's_{"_".join(version.split("."))}'
    cmd = '''python -c "from scripts.run_scripts.{} import run; run()"'''.format(file_name)
    c.run(cmd)

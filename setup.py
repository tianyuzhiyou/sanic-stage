from setuptools import setup, find_packages

with open('./src/requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='sanic-stage',
    version='0.0.2',
    description='web框架sanic脚手架封装',
    author='tianyuzhiyou',
    author_email="626004181@qq.com",
    packages=find_packages(),
    install_requires=required,
)
# sanic-stage

#### 介绍
基于python语言sanic的web脚手架，封装工业级的开箱即用的代码架构，引入consul,logging,sentry,jaeger,数据验证等。

#### 架构

python3.8 + sanic + celery + redis + sqlalchemy-corn 

#### 快速开始

- [下载代码](https://github.com/tianyuzhiyou/sanic-stage.git)

- 安装python3.8环境: 略

- 启动Web服务

```
cd sanic-stage

python web_server.py -a 0.0.0.0 -p 8000
```

打开浏览器输入：http://0.0.0.0:8000

- 启动celery服务

```
cd sanic-stage

celery -A celery_worker:celery_app worker --concurrency=3 -P celery_pool_asyncio:TaskPool
```

- 启动celery定时任务

```
cd sanic-stage

celery -A celery_worker:celery_app beat --scheduler celery_pool_asyncio:PersistentScheduler
```

- 启动脚本服务

```
cd sanic-stage

inv -c script_worker run-scripts-long
```

#### docker部署

##### 方式一：

- 下载镜像：[]()

- 启动docker

```
docker run -d -p 8000:8000 sanic-stage
```

打开浏览器输入：http://0.0.0.0:8000

##### 方式二

- docker构建镜像并启动

```
cd sanic-stage

docker build -t sanic-stage:1.0 . 

docker run -d -p 8000:8000 sanic-stage:1.0
```

##### 方式三

- docker-compose构建镜像并启动

```
cd sanic-stage

docker-compose -f docker-compose.yml up -d
```

#### 配置文件

```
config
├── __init__.py
├── basic.py
|── celery_config.py
└── local_config.py
```

- basic.py

```
ADD_REQUEST_LOG: bool,是否打印每个请求的详细日志，默认False

CONFIG_FROM_CONSUL: bool,是否开启从consul获取配置，默认False

SENTRY_DSN: url,sentry地址，配置后会自动将错误发送到sentry

ENABLE_DB: bool，是否开启连接数据库DB，默认为False，设置为True并且配置了MYSQL_CONFIG，将自动连接mysql

ENABLE_REDIS: bool，是否开启连接redis，默认为False，设置为True并且配置了REDIS_CONFIG，将自动连接redis
```

- celery_config.py

```
CELERY_TASKS： 异步任务定义所在的package列表，未被纳入列表的任务无效；
TASK_QUEUES：定义队列
CELERY_BROKER_URL： 设置rabbitmq的连接地址
CELERY_ROUTES：绑定异步任务和队列
CELERYBEAT_SCHEDULE： 定时任务注册
```

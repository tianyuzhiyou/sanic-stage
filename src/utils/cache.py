# -*- coding: utf-8 -*-

__all__ = [
    "RedisLockProxy",
    "RedisBitProxy",
    "RedisPfProxy",
    "RedisSetProxy",
    "RedisStrProxy",
    "RedisHashProxy",
    "RedisZsetProxy",
    "RedisProxy",
]

import time
from contextlib import asynccontextmanager
import asyncio
from typing import Any

from drivers.redis import redis_db
from utils.json_tool import json_dumps, json_loads


class RedisBaseProxy(object):

    def __init__(self, cache: Any = redis_db):
        self.redis_db = cache

    async def delete(self, key: str) -> int:
        """删除一个key"""
        num = await self.redis_db.common.delete(key)
        return num

    @property
    def client(self) -> Any:
        return self.redis_db.common

    async def safe_delete(self, key: str):
        """设置key失效"""
        await self.redis_db.common.expire(key, -1)


class RedisLockProxy(RedisBaseProxy):

    def __init__(self, cache: Any = redis_db):
        super().__init__(cache)
        self._lock_key = "lock:%s"
        self.locked = ""
        self.lock_timeout = False

    @asynccontextmanager
    async def with_lock(self, key: str, expire: int = 30, block_timeout=5, step=0.1):
        """
        @desc redis分布式锁是个下文管理器
        :param key: 缓存key
        :param expire: 锁失效时间
        :param step: 每次尝试获取锁的间隔
        :param block_timeout: 锁等待超时时间
        :return:
        for example:

        async with RedisLockProxy().with_lock("key_name") as lock:
            "do something"
        """
        try:
            t = await self.acquire_lock(key, expire, block_timeout, step)
            yield t
        finally:
            await self.release_lock(key)

    def check_lock_timeout(self, end_time):
        """检查是否锁等待超时"""
        if time.time() > end_time:
            self.lock_timeout = True
            raise ValueError("锁等待超时！")
        return False

    async def check_lock(self, key: str) -> str:
        """
        @desc 检查当前是否还拿到锁，此时如果获取到的时间戳没有改变，说明锁依旧有效;
        1. 该方法在程序逻辑中需要经常被调用，防止程序阻塞时，由于超时导致锁被自动释放；
        2. 尤其是在库存、金额一类的减扣操作，在加锁后操作完毕时，还需要再次检查是否还持有锁，如果已经失去锁，
        则考虑回滚操作，防止超卖发生；
        """
        timestamp = await self.client.get(self._lock_key % key)
        # 如果当前没有时间戳或者时间戳已经和记录的不相同，说明已经失去锁
        if not timestamp or str(timestamp.decode("utf-8")) != str(self.locked):
            self.locked = ""
        return self.locked

    async def acquire_lock(self, key: str, expire: int = 30, lock_timeout: int = 5, step: float = 0.03):
        """
        @desc 为当前KEY加锁, 默认30秒自动解锁,
        uri: https://redis.cn/commands/setnx.html
        1. 使用setnx命令，值为time.time()+expire+1,永久有效
        2. 获取锁的所有客户在锁返回0时，尝试去检查锁的过期时间，未过期则重复尝试；
        3. 过期后使用getset获取锁；
        4. 执行完程序后主动释放锁，但是有可能程序的执行时间大于上锁的时间，导致锁超时失效，被其它客户获取到。
        5. 因此对于可能存在的长耗时逻辑，如http请求，orm写请求等操作之后需要再次确认锁是否已经失效。
        """
        key = self._lock_key % key
        end_lock_time = time.time() + lock_timeout
        while 1:
            timestamp = str(time.time() + 1 + expire)
            # 尝试上锁
            if await self.client.setnx(key, timestamp):
                self.locked = timestamp
                return self.locked

            # 发现已经有锁，查看锁到期时间
            lock_timestamp = await self.client.get(key)
            # 发现当前时间大于锁的到期时间，重置锁的同时获取之前的时间戳，并记录新的时间戳
            if lock_timestamp and str(time.time()) > str(lock_timestamp.decode("utf-8")):
                old_timestamp = await self.client.getset(key, timestamp)
                # 如果时间戳没有发生改变，说明没有谁抢着上锁
                if lock_timestamp == old_timestamp:
                    self.locked = timestamp
                    return self.locked
            else:
                await asyncio.sleep(step)
                # 检查是否等待超时，超时抛出异常
                self.check_lock_timeout(end_lock_time)

    async def release_lock(self, key: str):
        """
        @desc 释放当前KEY的锁,需要检查当前是否还持有锁，极端情况下锁可能已经被其它客户获得，此时不应该释放
        """
        if self.lock_timeout:
            return True
        locked = await self.check_lock(key)
        if locked:
            # 只允许释放自己上的锁
            await self.client.delete(self._lock_key % key)


class RedisStrProxy(RedisBaseProxy):

    async def get(self, key: str) -> str:
        """获取字节类型"""
        data = await self.client.get(key)
        return data.decode("utf-8") if data else data

    async def set(self, key: str, value: str, ex: int = 10) -> bool:
        """设置字符串"""
        data = await self.client.set(key, value, expire=ex)
        return bool(data)

    async def get_data(self, key: str) -> Any:
        """
        @desc　反序列化json字符串
        """
        data = await self.client.get(key)
        if data is not None:
            try:
                data = json_loads(data)
            except:
                raise ValueError("非json结构数据")
        return data

    async def set_data(self, key: str, value: Any, ex: int = 0) -> bool:
        """
        @desc　使用字符串类型存储ｊｓｏｎ数据
        """
        try:
            value = json_dumps(value)
        except:
            raise ValueError("非json结构数据,无法序列化")
        return await self.client.set(key, value, expire=ex if ex else 0)


class RedisBitProxy(RedisBaseProxy):
    pass


class RedisPfProxy(RedisBaseProxy):
    pass


class RedisListProxy(RedisBaseProxy):
    pass


class RedisSetProxy(RedisBaseProxy):
    pass


class RedisHashProxy(RedisBaseProxy):
    pass


class RedisZsetProxy(RedisBaseProxy):
    pass


class RedisProxy(RedisZsetProxy,
                 RedisHashProxy,
                 RedisSetProxy,
                 RedisStrProxy,
                 RedisBitProxy,
                 RedisPfProxy,
                 RedisListProxy,
                 RedisLockProxy,
                 ):
    """
    @desc 聚合对外提供功能
    for examples:

    cache = RedisProxy()
    cache.get("key_name")
    """
    pass

from __future__ import annotations

import json
import time
from abc import ABC, abstractmethod
from typing import Any, Optional

from redis import Redis
from redis.exceptions import RedisError

from backend.app.core.config import Settings


class BaseCache(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        raise NotImplementedError


class MemoryCache(BaseCache):
    def __init__(self) -> None:
        self._store: dict[str, tuple[str, float]] = {}

    def get(self, key: str) -> Optional[str]:
        item = self._store.get(key)
        if not item:
            return None
        value, expires_at = item
        if expires_at < time.time():
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        self._store[key] = (value, time.time() + ttl_seconds)


class RedisCache(BaseCache):
    def __init__(self, client: Redis) -> None:
        self.client = client

    def get(self, key: str) -> Optional[str]:
        try:
            value = self.client.get(key)
            return value.decode("utf-8") if value is not None else None
        except RedisError:
            return None

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        try:
            self.client.setex(key, ttl_seconds, value)
        except RedisError:
            pass


def get_cache_backend(settings: Settings) -> BaseCache:
    if settings.redis_url:
        try:
            client = Redis.from_url(settings.redis_url)
            # ping to ensure connection
            client.ping()
            return RedisCache(client)
        except Exception:
            return MemoryCache()
    return MemoryCache()

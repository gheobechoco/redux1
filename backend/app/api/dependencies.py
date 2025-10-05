from __future__ import annotations

from functools import lru_cache
from typing import Generator

from backend.app.core.config import settings, Settings
from backend.app.core.cache import get_cache_backend, BaseCache
from backend.app.services.nasa_client import NasaClient
from backend.app.services.calculator import WeatherCalculator


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return settings


def get_cache() -> BaseCache:
    return get_cache_backend(settings)


@lru_cache(maxsize=1)
def get_nasa_client() -> NasaClient:
    return NasaClient(settings=get_settings(), cache=get_cache())


def get_calculator() -> WeatherCalculator:
    return WeatherCalculator(settings=get_settings(), cache=get_cache())

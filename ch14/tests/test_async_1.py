from pytest import *
from unittest.mock import AsyncMock, Mock, call
import async_1
import asyncio


@fixture
def mock_random(monkeypatch):
    random = Mock(random=Mock(return_value=0.5))
    monkeypatch.setattr(async_1, "random", random)
    return random


@fixture
def mock_sleep(monkeypatch):
    sleep = AsyncMock()
    monkeypatch.setattr(asyncio, "sleep", sleep)
    return sleep

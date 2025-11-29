import pytest
from unittest.mock import AsyncMock, Mock, call
import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import async_1


@pytest.fixture
def mock_random(monkeypatch):
    random = Mock(random=Mock(return_value=0.5))
    monkeypatch.setattr(async_1, "random", random)
    return random


@pytest.fixture
def mock_sleep(monkeypatch):
    sleep = AsyncMock()
    monkeypatch.setattr(asyncio, "sleep", sleep)
    return sleep


def test_random_sleep(mock_random, mock_sleep, capsys):
    asyncio.run(async_1.random_sleep(42))
    assert mock_random.random.mock_calls == [call()]
    mock_sleep.assert_awaited()
    mock_sleep.assert_called_once_with(2.5)
    out, err = capsys.readouterr()
    assert out.splitlines() == ["42 sleeps for 2.50 seconds", "42 awakens, refreshed"]


@pytest.fixture
def mock_random_sleep(monkeypatch):
    random_sleep = AsyncMock()
    monkeypatch.setattr(async_1, "random_sleep", random_sleep)
    return random_sleep


def test_sleepers(mock_random_sleep, capsys):
    asyncio.run(async_1.sleepers(2))
    mock_random_sleep.mock_calls == [call(0), call(1)]
    out, err = capsys.readouterr()
    assert out.splitlines() == ["Creating 2 tasks", "Waiting for 2 tasks"]


# ============================================================================
# EDGE CASES TESTS
# ============================================================================


class TestRandomSleepEdgeCases:
    """Edge case tests for random_sleep function."""

    def test_random_sleep_with_zero_counter(self, mock_random, mock_sleep, capsys):
        """Test random_sleep with counter value of 0."""
        asyncio.run(async_1.random_sleep(0))
        out, err = capsys.readouterr()
        assert "0 sleeps for 2.50 seconds" in out
        assert "0 awakens, refreshed" in out

    def test_random_sleep_with_negative_counter(self, mock_random, mock_sleep, capsys):
        """Test random_sleep with negative counter value."""
        asyncio.run(async_1.random_sleep(-5))
        out, err = capsys.readouterr()
        assert "-5 sleeps for 2.50 seconds" in out
        assert "-5 awakens, refreshed" in out

    def test_random_sleep_with_float_counter(self, mock_random, mock_sleep, capsys):
        """Test random_sleep with float counter value."""
        asyncio.run(async_1.random_sleep(3.14159))
        out, err = capsys.readouterr()
        assert "3.14159 sleeps for 2.50 seconds" in out
        assert "3.14159 awakens, refreshed" in out

    def test_random_sleep_with_string_counter(self, mock_random, mock_sleep, capsys):
        """Test random_sleep with string counter value."""
        asyncio.run(async_1.random_sleep("task_1"))
        out, err = capsys.readouterr()
        assert "task_1 sleeps for 2.50 seconds" in out
        assert "task_1 awakens, refreshed" in out

    def test_random_sleep_with_very_large_counter(
        self, mock_random, mock_sleep, capsys
    ):
        """Test random_sleep with very large counter value."""
        asyncio.run(async_1.random_sleep(999999999))
        out, err = capsys.readouterr()
        assert "999999999 sleeps for 2.50 seconds" in out
        assert "999999999 awakens, refreshed" in out

    def test_random_sleep_with_zero_delay(self, mock_sleep, capsys, monkeypatch):
        """Test random_sleep when random returns 0 (zero delay)."""
        random_mock = Mock(random=Mock(return_value=0.0))
        monkeypatch.setattr(async_1, "random", random_mock)

        asyncio.run(async_1.random_sleep(10))
        mock_sleep.assert_called_once_with(0.0)
        out, err = capsys.readouterr()
        assert "10 sleeps for 0.00 seconds" in out

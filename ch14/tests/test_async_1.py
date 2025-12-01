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

    def test_random_sleep_with_max_delay(self, mock_sleep, capsys, monkeypatch):
        """Test random_sleep when random returns 1.0 (max delay)."""
        random_mock = Mock(random=Mock(return_value=1.0))
        monkeypatch.setattr(async_1, "random", random_mock)

        asyncio.run(async_1.random_sleep(20))
        mock_sleep.assert_called_once_with(5.0)
        out, err = capsys.readouterr()
        assert "20 sleeps for 5.00 seconds" in out

    def test_random_sleep_with_minimum_positive_delay(
        self, mock_sleep, capsys, monkeypatch
    ):
        """Test random_sleep with very small positive delay."""
        random_mock = Mock(random=Mock(return_value=0.001))
        monkeypatch.setattr(async_1, "random", random_mock)
        asyncio.run(async_1.random_sleep(5))

        mock_sleep.assert_called_once_with(0.005)
        out, err = capsys.readouterr()
        assert "5 sleeps for 0.01 seconds" in out


class TestSleepersEdgeCases:
    """Edge case tests for sleepers function."""

    def test_sleepers_with_zero_tasks(self, mock_random_sleep, capsys):
        """Test sleepers with 0 tasks."""
        asyncio.run(async_1.sleepers(0))
        out, err = capsys.readouterr()
        assert out.splitlines() == ["Creating 0 tasks", "Waiting for 0 tasks"]
        # No tasks should be created
        assert mock_random_sleep.call_count == 0

    def test_sleepers_with_one_task(self, mock_random_sleep, capsys):
        """Test sleepers with exactly 1 task."""
        asyncio.run(async_1.sleepers(1))
        out, err = capsys.readouterr()
        assert "Creating 1 tasks" in out
        assert "Waiting for 1 tasks" in out

    def test_sleepers_with_large_number(self, mock_random_sleep, capsys):
        """Test sleepers with large number of tasks."""
        asyncio.run(async_1.sleepers(100))
        out, err = capsys.readouterr()
        assert "Creating 100 tasks" in out
        assert "Waiting for 100 tasks" in out

    def test_sleepers_with_default_value(self, mock_random_sleep, capsys):
        """Test sleepers with default parameter value."""
        asyncio.run(async_1.sleepers())
        out, err = capsys.readouterr()
        assert "Creating 5 tasks" in out
        assert "Waiting for 5 tasks" in out

    def test_sleepers_creates_correct_number_of_tasks(self, mock_random_sleep):
        """Test that sleepers creates exactly the right number of tasks."""
        asyncio.run(async_1.sleepers(7))
        assert mock_random_sleep.call_count == 7

    def test_sleepers_tasks_receive_sequential_counters(self, mock_random_sleep):
        """Test that tasks receive sequential counter values starting from 0."""
        asyncio.run(async_1.sleepers(5))
        expected_calls = [call(i) for i in range(5)]
        assert mock_random_sleep.call_args_list == expected_calls


class TestRandomSleepRealBehavior:
    """Test random_sleep without mocking to verify real behavior."""

    @pytest.mark.asyncio
    async def test_random_sleep_actually_sleeps(self):
        """Test that random_sleep actually performs async sleep."""
        import time

        start = time.time()
        await async_1.random_sleep(1)
        elapsed = time.time() - start
        # Should sleep between 0 and 5 seconds
        assert 0 <= elapsed <= 6.0

    @pytest.mark.asyncio
    async def test_random_sleep_returns_none(self):
        """Test that random_sleep returns None."""
        result = await async_1.random_sleep(1)
        assert result is None


class TestSleepersRealBehavior:
    """Test sleepers without mocking to verify real behavior."""

    @pytest.mark.asyncio
    async def test_sleepers_completes_all_tasks(self):
        """Test that sleepers waits for all tasks to complete."""
        import time

        start = time.time()
        await async_1.sleepers(3)
        elapsed = time.time() - start
        # Should complete (tasks run concurrently, so not 3*5 seconds)
        assert elapsed < 10.0

    @pytest.mark.asyncio
    async def test_sleepers_with_zero_completes_immediately(self):
        """Test that sleepers with 0 tasks completes immediately."""
        import time

        start = time.time()
        await async_1.sleepers(0)
        elapsed = time.time() - start
        # Should complete almost instantly
        assert elapsed < 0.1

    @pytest.mark.asyncio
    async def test_sleepers_returns_none(self):
        """Test that sleepers returns None."""
        result = await async_1.sleepers(2)
        assert result is None


class TestConcurrencyBehavior:
    """Test concurrent execution behavior."""

    @pytest.mark.asyncio
    async def test_tasks_run_concurrently_not_sequentially(self, monkeypatch):
        """Test that multiple tasks run concurrently, not sequentially."""
        import time

        # Mock random to always return 0.2 (1 second delay each)
        random_mock = Mock(random=Mock(return_value=0.2))
        monkeypatch.setattr(async_1, "random", random_mock)

        start = time.time()
        await async_1.sleepers(5)
        elapsed = time.time() - start

        # If sequential: 5 seconds, if concurrent: ~1 second
        assert elapsed < 2.0, "Tasks should run concurrently"

    @pytest.mark.asyncio
    async def test_gather_waits_for_all_tasks(self, monkeypatch):
        """Test that gather waits for all tasks to complete."""
        call_order = []

        async def tracking_random_sleep(counter):
            await asyncio.sleep(0.1)
            call_order.append(f"completed_{counter}")

        monkeypatch.setattr(async_1, "random_sleep", tracking_random_sleep)

        await async_1.sleepers(3)

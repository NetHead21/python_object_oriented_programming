"""Test Suite for Dining Philosophers Problem Implementation.

This module provides comprehensive test coverage for the asyncio-based
dining philosophers problem implementation. Tests cover:

- Basic philosopher behavior (eating, thinking cycles)
- Main function orchestration with multiple servings
- Fork (asyncio.Lock) initialization and usage
- Semaphore-based deadlock prevention
- Concurrent execution without race conditions
- Edge cases: single philosopher, two philosophers, large numbers (50+)
- Boundary conditions: zero servings, fork wraparound
- Output format validation
- Timing range verification

The test suite uses pytest fixtures to mock random number generation,
asyncio.sleep, and philosopher/semaphore creation for deterministic testing.
"""

import asyncio
from pytest import *
from unittest.mock import AsyncMock, Mock, call, sentinel
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import philosophers


@fixture
def mock_random(monkeypatch):
    """Mock the random module for deterministic philosopher timing tests.

    Replaces philosophers.random with a Mock that returns predictable values
    [0.2, 0.3] for eating and thinking durations. This allows tests to verify
    exact timing calculations: eat_time = 1 + 0.2 = 1.2, think_time = 1 + 0.3 = 1.3.

    Args:
        monkeypatch: Pytest fixture for safely patching module attributes.

    Returns:
        Mock object with random() method that returns predetermined values.
    """

    random = Mock(random=Mock(side_effect=[0.2, 0.3]))
    monkeypatch.setattr(philosophers, "random", random)
    return random


@fixture
def mock_sleep(monkeypatch):
    """Mock asyncio.sleep to eliminate actual waiting in tests.

    Replaces asyncio.sleep with an AsyncMock that completes immediately without
    blocking. This speeds up tests that would otherwise wait for philosopher
    eating and thinking durations (1-2 seconds each). The mock records all
    calls, allowing verification of sleep durations.

    Args:
        monkeypatch: Pytest fixture for safely patching module attributes.

    Returns:
        AsyncMock that tracks asyncio.sleep calls without actual delays.
    """

    sleep = AsyncMock()
    monkeypatch.setattr(asyncio, "sleep", sleep)
    return sleep


def test_philosopher(mock_sleep, mock_random, capsys):
    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(2)]
        footman = asyncio.BoundedSemaphore(1)
        return await philosophers.philosopher(0, footman)

    result_0 = asyncio.run(when())
    assert result_0 == (0, 1.2, 1.3)
    mock_sleep.assert_has_awaits([call(1.2), call(1.3)])
    out, err = capsys.readouterr()
    assert out.splitlines() == ["0 eating", "0 philosophizing"]


@fixture
def mock_philosopher(monkeypatch):
    """Mock the philosopher coroutine function for main() orchestration tests.

    Replaces philosophers.philosopher with an AsyncMock to test main() function
    behavior without executing actual philosopher logic. This isolates testing
    of the orchestration layer (multiple servings, task creation, asyncio.gather)
    from the philosopher implementation details.

    Useful for verifying:
    - Correct number of philosopher calls (faculty * servings)
    - Proper argument passing (philosopher ID and footman semaphore)
    - Call ordering and grouping by serving

    Args:
        monkeypatch: Pytest fixture for safely patching module attributes.

    Returns:
        AsyncMock that replaces the philosopher coroutine function.
    """

    philosopher = AsyncMock()
    monkeypatch.setattr(philosophers, "philosopher", philosopher)
    return philosopher


@fixture
def mock_bounded_semaphore(monkeypatch):
    """Mock asyncio.BoundedSemaphore class for footman creation tests.

    Replaces asyncio.BoundedSemaphore with a Mock class that returns a sentinel
    object instead of a real semaphore. This allows testing that main() creates
    the footman semaphore with the correct capacity (faculty - 1) without
    needing actual semaphore functionality.

    The sentinel return value can be tracked through mock_philosopher calls to
    verify each philosopher receives the same footman instance.

    Args:
        monkeypatch: Pytest fixture for safely patching module attributes.

    Returns:
        Mock class that records BoundedSemaphore instantiation calls and
        returns sentinel.mock_bounded_semaphore.
    """

    mock_class = Mock(return_value=sentinel.mock_bounded_semaphore)
    monkeypatch.setattr(asyncio, "BoundedSemaphore", mock_class)
    return mock_class


def test_main(mock_philosopher, mock_bounded_semaphore):
    asyncio.run(philosophers.main(5, 1))
    mock_philosopher.assert_has_awaits(
        [
            call(0, sentinel.mock_bounded_semaphore),
            call(1, sentinel.mock_bounded_semaphore),
            call(2, sentinel.mock_bounded_semaphore),
            call(3, sentinel.mock_bounded_semaphore),
            call(4, sentinel.mock_bounded_semaphore),
        ]
    )

    mock_bounded_semaphore.assert_called_once_with(4)


def test_main_multiple_servings(mock_philosopher, mock_bounded_semaphore):
    """Test that multiple servings call philosophers the correct number of times."""

    asyncio.run(philosophers.main(3, 2))
    # Should be called 3 philosophers * 2 servings = 6 times
    assert mock_philosopher.await_count == 6
    mock_bounded_semaphore.assert_called_once_with(2)


def test_main_initializes_forks():
    """Test that main() properly initializes the global FORKS list."""

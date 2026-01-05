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

    asyncio.run(philosophers.main(5, 1))
    assert len(philosophers.FORKS) == 5
    assert all(isinstance(fork, asyncio.Lock) for fork in philosophers.FORKS)


def test_main_creates_correct_semaphore_size(mock_philosopher, mock_bounded_semaphore):
    """Test that footman semaphore is created with faculty-1 capacity."""

    asyncio.run(philosophers.main(10, 1))
    mock_bounded_semaphore.assert_called_once_with(9)


def test_philosopher_concurrent_execution(mock_sleep):
    """Test multiple philosophers running concurrently without deadlock."""

    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(5)]
        footman = asyncio.BoundedSemaphore(4)
        tasks = [philosophers.philosopher(i, footman) for i in range(5)]
        return await asyncio.gather(*tasks)

    results = asyncio.run(when())
    assert len(results) == 5
    # Each result should be a tuple of (id, eat_time, think_time)

    for i, (phil_id, eat_time, think_time) in enumerate(results):
        assert phil_id == i
        assert 1.0 <= eat_time < 2.0
        assert 1.0 <= think_time < 2.0


def test_philosopher_uses_correct_forks(mock_sleep):
    """Test that philosopher uses the correct pair of adjacent forks."""

    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(5)]
        footman = asyncio.BoundedSemaphore(4)

        # Try to acquire philosopher 0's forks manually
        async with philosophers.FORKS[0]:
            # Philosopher 0 should be blocked because we hold fork 0
            task = asyncio.create_task(philosophers.philosopher(0, footman))
            await asyncio.sleep(0.1)
            assert not task.done()
            task.cancel()

        return True

    result = asyncio.run(when())
    assert result


def test_philosopher_returns_correct_format(mock_sleep, mock_random):
    """Test that philosopher returns a properly formatted tuple."""

    mock_random.random.side_effect = [0.5, 0.7]

    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(3)]
        footman = asyncio.BoundedSemaphore(2)
        return await philosophers.philosopher(1, footman)

    result = asyncio.run(when())
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert result[0] == 1
    assert result[1] == 1.5
    assert result[2] == 1.7


def test_philosopher_output_format(mock_sleep, mock_random, capsys):
    """Test that philosopher prints correct messages in correct order."""

    mock_random.random.side_effect = [0.1, 0.2]

    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(3)]
        footman = asyncio.BoundedSemaphore(2)
        await philosophers.philosopher(2, footman)

    asyncio.run(when())
    out, err = capsys.readouterr()
    lines = out.splitlines()
    assert lines == ["2 eating", "2 philosophizing"]


# Edge Case Tests


def test_edge_case_two_philosophers(mock_sleep):
    """Edge case: minimum meaningful scenario with 2 philosophers."""

    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(2)]
        footman = asyncio.BoundedSemaphore(1)  # Only 1 can eat at a time
        tasks = [philosophers.philosopher(i, footman) for i in range(2)]
        return await asyncio.gather(*tasks)

    results = asyncio.run(when())
    assert len(results) == 2
    assert results[0][0] == 0
    assert results[1][0] == 1


def test_edge_case_single_philosopher(mock_sleep):
    """Edge case: single philosopher (degenerate case, but should work)."""

    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(1)]
        footman = asyncio.BoundedSemaphore(0)  # faculty - 1 = 0
        # Single philosopher will wait forever on semaphore with limit 0
        # So we need to use a timeout

        try:
            task = asyncio.wait_for(philosophers.philosopher(0, footman), timeout=0.1)
            return await task
        except asyncio.TimeoutError:
            return "timeout"

    result = asyncio.run(when())
    # With semaphore(0), the philosopher will be blocked
    assert result == "timeout"


def test_edge_case_large_faculty(mock_sleep):
    """Edge case: large number of philosophers (50)."""

    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(50)]
        footman = asyncio.BoundedSemaphore(49)
        tasks = [philosophers.philosopher(i, footman) for i in range(50)]
        return await asyncio.gather(*tasks)

    results = asyncio.run(when())
    assert len(results) == 50

    # Verify all philosophers completed
    philosopher_ids = {result[0] for result in results}
    assert philosopher_ids == set(range(50))


def test_edge_case_zero_servings(mock_philosopher):
    """Edge case: zero servings should not call philosopher at all."""

    asyncio.run(philosophers.main(5, 0))
    mock_philosopher.assert_not_awaited()


def test_edge_case_fork_wraparound(mock_sleep):
    """Test that last philosopher correctly uses fork[0] (wraparound)."""

    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(5)]
        footman = asyncio.BoundedSemaphore(4)

        # Last philosopher (id=4) should use forks 4 and 0
        # Lock fork 0 to verify philosopher 4 needs it
        async with philosophers.FORKS[0]:
            task = asyncio.create_task(philosophers.philosopher(4, footman))
            await asyncio.sleep(0.1)
            assert not task.done()
            task.cancel()

        return True

    result = asyncio.run(when())
    assert result


def test_deadlock_prevention_with_full_faculty():
    """Test that footman semaphore prevents deadlock with all philosophers."""

    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(5)]

        # If we didn't have the footman, all 5 could deadlock
        # With footman set to 4, at least one can't start, preventing deadlock
        footman = asyncio.BoundedSemaphore(4)

        tasks = [philosophers.philosopher(i, footman) for i in range(5)]
        # This should complete without deadlock

        results = await asyncio.wait_for(asyncio.gather(*tasks), timeout=10.0)
        return results

    results = asyncio.run(when())
    assert len(results) == 5
    # All philosophers should complete successfully


def test_main_with_single_serving_output(capsys):
    """Test main output format with real execution (single serving)."""

    asyncio.run(philosophers.main(3, 1))
    out, err = capsys.readouterr()
    lines = out.splitlines()

    # Should have eating/philosophizing messages plus results list
    eating_lines = [line for line in lines if "eating" in line]
    philosophizing_lines = [line for line in lines if "philosophizing" in line]
    result_lines = [line for line in lines if line.startswith("[")]

    assert len(eating_lines) == 3
    assert len(philosophizing_lines) == 3
    assert len(result_lines) == 1


def test_philosopher_timing_ranges(mock_random, mock_sleep):
    """Test that eating and thinking times are in expected range [1.0, 2.0)."""

    mock_random.random.side_effect = [0.0, 0.999999]

    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(2)]
        footman = asyncio.BoundedSemaphore(1)
        return await philosophers.philosopher(0, footman)

    result = asyncio.run(when())
    _, eat_time, think_time = result
    assert eat_time == 1.0
    assert abs(think_time - 1.999999) < 0.000001
    assert 1.0 <= eat_time < 2.0
    assert 1.0 <= think_time < 2.0


def test_concurrent_fork_access_safety():
    """Test that forks (locks) properly prevent concurrent access."""

    async def when():
        philosophers.FORKS = [asyncio.Lock() for i in range(3)]
        footman = asyncio.BoundedSemaphore(2)

        # Create a shared counter to verify mutual exclusion
        counter = {"value": 0}

        async def check_philosopher(id: int):
            async with footman:
                async with philosophers.FORKS[id], philosophers.FORKS[(id + 1) % 3]:
                    # Critical section - increment counter
                    old_value = counter["value"]
                    await asyncio.sleep(0.01)  # Simulate work
                    counter["value"] = old_value + 1

        tasks = [check_philosopher(i) for i in range(3)]
        await asyncio.gather(*tasks)
        return counter["value"]

    result = asyncio.run(when())
    # If locks work correctly, counter should be 3
    assert result == 3


def test_main_forks_reset_between_runs():
    """Test that FORKS are properly reinitialized on each main() call."""

    asyncio.run(philosophers.main(3, 1))
    forks_first = philosophers.FORKS

    asyncio.run(philosophers.main(5, 1))
    forks_second = philosophers.FORKS

    # Different runs should create different fork objects
    assert len(forks_first) == 3
    assert len(forks_second) == 5
    assert forks_first is not forks_second

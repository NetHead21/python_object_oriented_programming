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

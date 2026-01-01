"""Dining Philosophers Problem - Asyncio Implementation.

This module demonstrates a solution to the classic dining philosophers problem
using Python's asyncio library. The problem involves N philosophers seated at a
round table with N forks, where each philosopher needs two forks to eat.

The implementation uses:
- asyncio.Lock to represent each fork (prevents race conditions)
- asyncio.BoundedSemaphore ("footman") to limit concurrent diners to N-1,
  preventing deadlock by ensuring at least one philosopher can always acquire
  both forks.

Each philosopher cycles through eating and thinking phases, with randomized
durations to simulate non-deterministic behavior.
"""

from __future__ import annotations
import asyncio
import random
from typing import List

FORKS: List[asyncio.Lock]
"""Global list of asyncio.Lock objects representing forks at the table.

Each fork is shared between two adjacent philosophers. Philosopher i uses
FORKS[i] and FORKS[(i+1) % len(FORKS)] to eat. This wraps around so the
last philosopher shares a fork with the first.

Initialized in main() to match the number of philosophers (faculty).
"""


async def philosopher(id: int, footman: asyncio.Semaphore) -> tuple[int, float, float]:
    """Simulate a single philosopher's dining cycle: eating, then thinking.

    The philosopher first acquires permission from the footman (semaphore) to
    approach the table, then acquires both adjacent forks (locks) to eat.
    After eating, they release the forks and spend time thinking before
    returning their results.

    The footman semaphore limits the number of concurrent diners to N-1,
    preventing deadlock. Without this, all N philosophers could grab their
    left fork simultaneously, deadlocking as they wait for their right fork.

    Args:
        id: Zero-based integer identifier for this philosopher, determining
            which forks (FORKS[id] and FORKS[(id+1) % N]) they use.
        footman: asyncio.BoundedSemaphore with limit of (faculty - 1) that
            controls how many philosophers can attempt to eat concurrently.

    Returns:
        A tuple of (philosopher_id, eating_duration, thinking_duration) where
        durations are floats in the range [1.0, 2.0) seconds.

    Side Effects:
        Prints "{id} eating" when eating begins and "{id} philosophizing"
        when thinking begins. These print statements allow external observers
        to track the state of each philosopher.
    """
    async with footman:
        async with FORKS[id], FORKS[(id + 1) % len(FORKS)]:
            eat_time = 1 + random.random()
            print(f"{id} eating")
            await asyncio.sleep(eat_time)
        think_time = 1 + random.random()
        print(f"{id} philosophizing")
        await asyncio.sleep(think_time)
    return id, eat_time, think_time


async def main(faculty: int = 5, servings: int = 5) -> None:
    """Run the dining philosophers simulation for multiple rounds.

    Sets up the table with forks (asyncio.Lock objects) and a footman
    (asyncio.BoundedSemaphore) to prevent deadlock, then runs multiple
    "servings" where all philosophers eat and think concurrently.

    Each serving represents one complete round where every philosopher
    gets one turn to eat and think. The asyncio.gather() call ensures
    all philosophers in a serving complete before the next serving begins.

    Args:
        faculty: Number of philosophers (and forks) at the table. Default is 5.
            Must be at least 2 for the problem to be meaningful.
        servings: Number of rounds (eat/think cycles) each philosopher will
            complete. Default is 5.

    Side Effects:
        - Initializes the global FORKS list with asyncio.Lock objects
        - Prints philosopher state changes ("{id} eating", "{id} philosophizing")
        - Prints the results list after each serving, showing tuples of
          (philosopher_id, eat_time, think_time) for all philosophers

    Example Output:
        0 eating
        1 eating
        2 eating
        3 eating
        0 philosophizing
        4 eating
        1 philosophizing
        ...
        [(0, 1.23, 1.45), (1, 1.67, 1.89), ...]
    """

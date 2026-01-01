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

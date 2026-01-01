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

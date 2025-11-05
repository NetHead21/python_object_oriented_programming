"""Comprehensive Guide to Concurrency and Parallelism in Python.

This module demonstrates various approaches to concurrent and parallel programming
in Python, including threading, multiprocessing, asyncio, and concurrent.futures.

Concurrency vs Parallelism:
    - Concurrency: Multiple tasks making progress (not necessarily simultaneously)
    - Parallelism: Multiple tasks executing simultaneously on multiple CPU cores

Key Concepts:
    1. Threading: Concurrent execution, good for I/O-bound tasks
    2. Multiprocessing: True parallelism, good for CPU-bound tasks
    3. AsyncIO: Cooperative multitasking, excellent for I/O-bound operations
    4. Concurrent.futures: High-level interface for threading and multiprocessing
"""

import threading
import multiprocessing
import asyncio
import time
import concurrent.futures
from typing import List, Any
from queue import Queue


# ============================================================================
# SECTION 1: THREADING - CONCURRENT EXECUTION (I/O-BOUND TASKS)
# ============================================================================


class ThreadingExamples:
    """Examples demonstrating Python threading for concurrent execution.

    Threading is best for I/O-bound tasks where the program spends time waiting
    for external resources (network, disk, user input). Python's GIL (Global
    Interpreter Lock) prevents true parallel execution of Python bytecode, but
    threads can run concurrently during I/O operations.
    """

    @staticmethod
    def basic_thread_example() -> None:
        """Demonstrate basic thread creation and execution.

        Example:
            >>> ThreadingExamples.basic_thread_example()
            Thread Thread-1 starting work...
            Thread Thread-2 starting work...
            Main thread continues...
            Thread Thread-1 completed
            Thread Thread-2 completed
            All threads finished
        """

        def worker(thread_id: int, duration: float) -> None:
            """Simulates work by sleeping for a duration."""
            print(f"Thread {threading.current_thread().name} starting work...")
            time.sleep(duration)
            print(f"Thread {threading.current_thread().name} completed")

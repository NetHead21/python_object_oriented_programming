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

        # Create threads
        thread1 = threading.Thread(target=worker, args=(1, 2))
        thread2 = threading.Thread(target=worker, args=(2, 1))

        # Start threads
        thread1.start()
        thread2.start()

        print("Main thread continues...")

        # Wait for threads to complete
        thread1.join()
        thread2.join()

        print("All threads finished")

    @staticmethod
    def thread_with_lock() -> None:
        """Demonstrate thread synchronization using locks to prevent race conditions.

        Locks ensure that only one thread can access shared resources at a time,
        preventing data corruption from simultaneous access.

        Example:
            >>> ThreadingExamples.thread_with_lock()
            Final counter value: 100000
        """

        counter = 0
        lock = threading.Lock()

        def increment_counter(iterations: int) -> None:
            """Safely increment a shared counter using a lock."""
            nonlocal counter
            for _ in range(iterations):
                with lock:  # Acquire lock automatically
                    counter += 1

        threads = []
        for _ in range(10):
            thread = threading.Thread(target=increment_counter, args=(10000,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print(f"Final counter value: {counter}")

    @staticmethod
    def producer_consumer_pattern() -> None:
        """Demonstrate producer-consumer pattern using Queue.

        The Queue class is thread-safe and provides a simple way to pass data
        between threads without explicit locking.

        Example:
            >>> ThreadingExamples.producer_consumer_pattern()
            Producer: Added item 0 to queue
            Consumer: Processing item 0
            Producer: Added item 1 to queue
            ...
        """

        queue: Queue = Queue(maxsize=5)

        def producer(num_items: int) -> None:
            """Produces items and adds them to the queue."""
            for i in range(num_items):
                item = f"item {i}"
                queue.put(item)
                print(f"Producer: Added {item} to queue")
                time.sleep(0.1)
            # Signal completion
            queue.put(None)

        def consumer() -> None:
            """Consumes items from the queue until receiving None."""
            while True:
                item = queue.get()
                if item is None:
                    break
                print(f"Consumer: Processing {item}")
                time.sleep(0.2)
                queue.task_done()

        producer_thread = threading.Thread(target=producer, args=(10,))
        consumer_thread = threading.Thread(target=consumer)

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()


class ThreadPoolExample:
    """Examples using ThreadPoolExecutor for managing thread pools.

    ThreadPoolExecutor provides a high-level interface for asynchronously
    executing callables using a pool of worker threads.
    """

    @staticmethod
    def download_simulation(urls: List[str]) -> List[str]:
        """Simulate downloading multiple URLs concurrently.

        Args:
            urls: List of URLs to "download"

        Returns:
            List of results from each download

        Example:
            >>> urls = [f"http://example.com/page{i}" for i in range(5)]
            >>> results = ThreadPoolExample.download_simulation(urls)
            >>> len(results)
            5
        """

        def fetch_url(url: str) -> str:
            """Simulates downloading a URL."""
            print(f"Starting download: {url}")
            time.sleep(1)  # Simulate network delay
            print(f"Completed download: {url}")
            return f"Content from {url}"

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Submit all tasks and get futures
            futures = [executor.submit(fetch_url, url) for url in urls]

            # Wait for all futures to complete and collect results
            results = [future.result() for future in futures]

        return results

    @staticmethod
    def map_example() -> List[int]:
        """Demonstrate using map() for parallel execution.

        The map() method is useful when you want to apply a function to
        multiple inputs and collect the results.

        Returns:
            List of processed results
        """

        def process_item(item: int) -> int:
            """Simulates processing an item."""
            time.sleep(0.5)
            return item * item

        items = list(range(10))

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(process_item, items))

        return results


# ============================================================================
# SECTION 2: MULTIPROCESSING - TRUE PARALLELISM (CPU-BOUND TASKS)
# ============================================================================


class MultiprocessingExamples:
    """Examples demonstrating multiprocessing for CPU-bound tasks.

    Multiprocessing bypasses the GIL by using separate Python processes,
    enabling true parallel execution on multiple CPU cores. Best for
    CPU-intensive computations.
    """

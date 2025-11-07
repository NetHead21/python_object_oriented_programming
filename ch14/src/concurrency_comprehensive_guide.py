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

    @staticmethod
    def cpu_intensive_task(n: int) -> int:
        """Simulates a CPU-intensive computation.

        Args:
            n: Upper limit for computation

        Returns:
            Sum of squares up to n
        """
        result = 0
        for i in range(n):
            result += i * i
        return result

    @staticmethod
    def basic_process_example() -> None:
        """Demonstrate basic process creation and execution.

        Example:
            >>> MultiprocessingExamples.basic_process_example()
            Process 1 computing...
            Process 2 computing...
            Results: [328350, 328350]
        """

        def worker(process_id: int, n: int, results: List) -> None:
            """Worker function for process."""
            print(f"Process {process_id} computing...")
            result = MultiprocessingExamples.cpu_intensive_task(n)
            results.append(result)

        # Using Manager for shared list
        with multiprocessing.Manager() as manager:
            results = manager.list()

            process1 = multiprocessing.Process(target=worker, args=(1, 1000, results))
            process2 = multiprocessing.Process(target=worker, args=(2, 1000, results))

            process1.start()
            process2.start()

            process1.join()
            process2.join()

            print(f"Results: {list(results)}")

    @staticmethod
    def process_pool_example(numbers: List[int]) -> List[int]:
        """Demonstrate using ProcessPoolExecutor for parallel computation.

        Args:
            numbers: List of numbers to process

        Returns:
            List of results from parallel computation

        Example:
            >>> numbers = [1000, 2000, 3000, 4000]
            >>> results = MultiprocessingExamples.process_pool_example(numbers)
            >>> len(results) == len(numbers)
            True
        """

        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            results = list(
                executor.map(MultiprocessingExamples.cpu_intensive_task, numbers)
            )
        return results

    @staticmethod
    def compare_sequential_vs_parallel() -> None:
        """Compare execution time of sequential vs parallel processing.

        Demonstrates the performance benefit of parallelism for CPU-bound tasks.
        """

        numbers = [5000000] * 8

        # Sequential execution
        start_time = time.time()
        _ = [MultiprocessingExamples.cpu_intensive_task(n) for n in numbers]
        sequential_time = time.time() - start_time

        # Parallel execution
        start_time = time.time()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            _ = list(executor.map(MultiprocessingExamples.cpu_intensive_task, numbers))
        parallel_time = time.time() - start_time

        print(f"Sequential time: {sequential_time:.2f} seconds")
        print(f"Parallel time: {parallel_time:.2f} seconds")
        print(f"Speedup: {sequential_time / parallel_time:.2f}x")


class ProcessCommunication:
    """Examples of inter-process communication patterns."""

    @staticmethod
    def queue_communication() -> None:
        """Demonstrate process communication using Queue.

        Queue provides a thread and process-safe FIFO data structure
        for passing messages between processes.
        """

        def producer(queue: multiprocessing.Queue, items: List[Any]) -> None:
            """Produces items and puts them in the queue."""
            for item in items:
                queue.put(item)
                print(f"Produced: {item}")
                time.sleep(0.1)
            queue.put(None)  # Sentinel value

        def consumer(queue: multiprocessing.Queue) -> None:
            """Consumes items from the queue."""
            while True:
                item = queue.get()
                if item is None:
                    break
                print(f"Consumed: {item}")
                time.sleep(0.2)

        queue = multiprocessing.Queue()
        items = list(range(10))

        prod = multiprocessing.Process(target=producer, args=(queue, items))
        cons = multiprocessing.Process(target=consumer, args=(queue,))

        prod.start()
        cons.start()

        prod.join()
        cons.join()

    @staticmethod
    def pipe_communication() -> None:
        """Demonstrate bi-directional communication using Pipe.

        Pipe creates a pair of connection objects for two-way communication
        between processes.
        """

        def worker(conn: multiprocessing.connection.Connection) -> None:
            """Worker process that communicates via pipe."""
            # Receive message
            msg = conn.recv()
            print(f"Worker received: {msg}")

            # Send response
            conn.send(f"Processed: {msg}")
            conn.close()

        parent_conn, child_conn = multiprocessing.Pipe()

        process = multiprocessing.Process(target=worker, args=(child_conn,))
        process.start()

        # Send message from parent
        parent_conn.send("Hello from parent")

        # Receive response
        response = parent_conn.recv()
        print(f"Parent received: {response}")

        process.join()


# ============================================================================
# SECTION 3: ASYNCIO - ASYNCHRONOUS I/O (COOPERATIVE MULTITASKING)
# ============================================================================


class AsyncIOExamples:
    """Examples demonstrating asyncio for asynchronous programming.

    AsyncIO uses cooperative multitasking with coroutines, allowing efficient
    handling of I/O-bound operations without threads or processes. Perfect for
    network programming, web scraping, and handling many concurrent connections.
    """

    @staticmethod
    async def async_task(task_id: int, duration: float) -> str:
        """Simulates an asynchronous task.

        Args:
            task_id: Identifier for the task
            duration: How long the task takes

        Returns:
            Result message
        """
        print(f"Task {task_id} started")
        await asyncio.sleep(duration)  # Non-blocking sleep
        print(f"Task {task_id} completed")
        return f"Result from task {task_id}"

    @staticmethod
    async def run_concurrent_tasks() -> List[str]:
        """Run multiple async tasks concurrently.

        Returns:
            List of results from all tasks

        Example:
            >>> asyncio.run(AsyncIOExamples.run_concurrent_tasks())
            Task 1 started
            Task 2 started
            Task 3 started
            ...
        """
        # Create multiple tasks
        tasks = [
            asyncio.create_task(AsyncIOExamples.async_task(1, 2)),
            asyncio.create_task(AsyncIOExamples.async_task(2, 1)),
            asyncio.create_task(AsyncIOExamples.async_task(3, 3)),
        ]

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        return results

    @staticmethod
    async def fetch_data_async(url: str) -> str:
        """Simulates fetching data asynchronously.

        Args:
            url: URL to fetch

        Returns:
            Fetched data
        """
        print(f"Fetching {url}...")
        await asyncio.sleep(1)  # Simulate network delay
        print(f"Completed {url}")
        return f"Data from {url}"

    @staticmethod
    async def fetch_multiple_urls(urls: List[str]) -> List[str]:
        """Fetch multiple URLs concurrently using asyncio.

        Args:
            urls: List of URLs to fetch

        Returns:
            List of fetched data
        """
        tasks = [AsyncIOExamples.fetch_data_async(url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

    @staticmethod
    async def async_generator_example() -> None:
        """Demonstrate async generators for streaming data.

        Async generators allow you to produce values asynchronously,
        useful for processing streams of data.
        """

        async def async_range(count: int):
            """Async generator that yields numbers."""
            for i in range(count):
                await asyncio.sleep(0.1)
                yield i

        # Consume async generator
        print("Async generator output:")
        async for value in async_range(5):
            print(f"Received: {value}")

    @staticmethod
    async def async_context_manager() -> None:
        """Demonstrate async context managers.

        Async context managers use __aenter__ and __aexit__ methods
        for resource management in async code.
        """

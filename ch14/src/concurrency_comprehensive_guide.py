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

        class AsyncResource:
            """Example async context manager."""

            async def __aenter__(self):
                """Async enter method."""
                print("Acquiring async resource...")
                await asyncio.sleep(0.5)
                print("Resource acquired")
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                """Async exit method."""
                print("Releasing async resource...")
                await asyncio.sleep(0.5)
                print("Resource released")

            async def use_resource(self):
                """Use the resource."""
                print("Using resource...")
                await asyncio.sleep(1)

        async with AsyncResource() as resource:
            await resource.use_resource()


# ============================================================================
# SECTION 4: PRACTICAL PATTERNS AND BEST PRACTICES
# ============================================================================


class ConcurrencyPatterns:
    """Common concurrency patterns and best practices."""

    @staticmethod
    def timeout_pattern() -> None:
        """Demonstrate timeout pattern for long-running operations.

        Timeouts prevent operations from hanging indefinitely.
        """

        def long_running_task():
            """Simulates a long-running task."""
            time.sleep(10)
            return "Task completed"

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(long_running_task)
            try:
                result = future.result(timeout=2)  # 2-second timeout
                print(f"Result: {result}")
            except concurrent.futures.TimeoutError:
                print("Task timed out!")

    @staticmethod
    async def async_timeout_pattern() -> None:
        """Demonstrate async timeout pattern.

        AsyncIO provides built-in timeout support for async operations.
        """

        async def slow_operation():
            """Simulates a slow async operation."""
            await asyncio.sleep(5)
            return "Operation completed"

        try:
            result = await asyncio.wait_for(slow_operation(), timeout=2.0)
            print(f"Result: {result}")
        except asyncio.TimeoutError:
            print("Async operation timed out!")

    @staticmethod
    def semaphore_pattern() -> None:
        """Demonstrate semaphore for limiting concurrent access.

        Semaphores control the number of threads that can access a resource
        simultaneously, useful for rate limiting.
        """

        semaphore = threading.Semaphore(3)  # Max 3 concurrent accesses

        def limited_access(worker_id: int):
            """Function with limited concurrent access."""
            with semaphore:
                print(f"Worker {worker_id} acquired semaphore")
                time.sleep(2)
                print(f"Worker {worker_id} releasing semaphore")

        threads = []
        for i in range(10):
            thread = threading.Thread(target=limited_access, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    @staticmethod
    def future_callback_pattern() -> None:
        """Demonstrate callbacks with futures.

        Callbacks allow you to specify code to run when a future completes,
        useful for handling results asynchronously.
        """

        def task(n: int) -> int:
            """Simple task that squares a number."""
            time.sleep(1)
            return n * n

        def callback(future: concurrent.futures.Future):
            """Callback function executed when future completes."""
            result = future.result()
            print(f"Callback received result: {result}")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(task, 5)
            future.add_done_callback(callback)
            # Wait for completion
            concurrent.futures.wait([future])


class ErrorHandling:
    """Examples of error handling in concurrent code."""

    @staticmethod
    def thread_exception_handling() -> None:
        """Demonstrate exception handling in threads.

        Exceptions in threads don't propagate to the main thread,
        so they must be caught and handled within the thread.
        """

        exceptions = []
        lock = threading.Lock()

        def risky_task(task_id: int):
            """Task that may raise an exception."""
            try:
                if task_id % 2 == 0:
                    raise ValueError(f"Error in task {task_id}")
                print(f"Task {task_id} completed successfully")
            except Exception as e:
                with lock:
                    exceptions.append((task_id, str(e)))

        threads = []
        for i in range(5):
            thread = threading.Thread(target=risky_task, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        if exceptions:
            print("Exceptions caught:")
            for task_id, error in exceptions:
                print(f"  Task {task_id}: {error}")

    @staticmethod
    def future_exception_handling() -> None:
        """Demonstrate exception handling with futures.

        Futures capture exceptions, which can be retrieved when
        calling result() or checked with exception().
        """

        def failing_task(n: int) -> int:
            """Task that may fail."""
            if n < 0:
                raise ValueError("Negative number not allowed")
            return n * n

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(failing_task, i) for i in [-1, 2, -3, 4]]

            for i, future in enumerate(futures):
                try:
                    result = future.result()
                    print(f"Task {i}: Result = {result}")
                except Exception as e:
                    print(f"Task {i}: Exception = {e}")

    @staticmethod
    async def async_exception_handling() -> None:
        """Demonstrate exception handling in async code."""

        async def risky_async_task(task_id: int):
            """Async task that may raise an exception."""
            await asyncio.sleep(0.1)
            if task_id % 2 == 0:
                raise ValueError(f"Error in async task {task_id}")
            return f"Success: {task_id}"

        tasks = [risky_async_task(i) for i in range(5)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Task {i}: Exception = {result}")
            else:
                print(f"Task {i}: Result = {result}")


# ============================================================================
# SECTION 5: PERFORMANCE COMPARISON AND GUIDELINES
# ============================================================================


class PerformanceComparison:
    """Compare different concurrency approaches."""

    @staticmethod
    def io_bound_comparison(num_tasks: int = 10) -> None:
        """Compare threading vs asyncio for I/O-bound tasks.

        Args:
            num_tasks: Number of I/O tasks to simulate
        """

        def io_task():
            """Simulates I/O operation."""
            time.sleep(0.5)

        async def async_io_task():
            """Async version of I/O task."""
            await asyncio.sleep(0.5)

        # Sequential
        start = time.time()
        for _ in range(num_tasks):
            io_task()
        sequential_time = time.time() - start

        # Threading
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(io_task) for _ in range(num_tasks)]
            concurrent.futures.wait(futures)
        threading_time = time.time() - start

        # AsyncIO
        async def run_async():
            tasks = [async_io_task() for _ in range(num_tasks)]
            await asyncio.gather(*tasks)

        start = time.time()
        asyncio.run(run_async())
        asyncio_time = time.time() - start

        print(f"I/O-Bound Task Comparison ({num_tasks} tasks):")
        print(f"  Sequential: {sequential_time:.2f}s")
        print(f"  Threading:  {threading_time:.2f}s")
        print(f"  AsyncIO:    {asyncio_time:.2f}s")

    @staticmethod
    def cpu_bound_comparison(num_tasks: int = 8) -> None:
        """Compare threading vs multiprocessing for CPU-bound tasks.

        Args:
            num_tasks: Number of CPU tasks to run
        """

        def cpu_task():
            """CPU-intensive computation."""
            result = 0
            for i in range(10000000):
                result += i * i
            return result

        # Sequential
        start = time.time()
        _ = [cpu_task() for _ in range(num_tasks)]
        sequential_time = time.time() - start

        # Threading (won't help due to GIL)
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            _ = list(executor.map(lambda _: cpu_task(), range(num_tasks)))
        threading_time = time.time() - start

        # Multiprocessing (true parallelism)
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            _ = list(executor.map(lambda _: cpu_task(), range(num_tasks)))
        multiprocessing_time = time.time() - start

        print(f"CPU-Bound Task Comparison ({num_tasks} tasks):")
        print(f"  Sequential:      {sequential_time:.2f}s")
        print(f"  Threading:       {threading_time:.2f}s")
        print(f"  Multiprocessing: {multiprocessing_time:.2f}s")


# ============================================================================
# GUIDELINES AND BEST PRACTICES
# ============================================================================


def print_guidelines() -> None:
    """Print guidelines for choosing concurrency approaches."""
    guidelines = """
    ============================================================
    CONCURRENCY AND PARALLELISM GUIDELINES
    ============================================================
    
    WHEN TO USE THREADING:
    ✓ I/O-bound tasks (network requests, file I/O, database queries)
    ✓ Need to share memory between concurrent operations
    ✓ Working with libraries that release the GIL (NumPy, some C extensions)
    ✗ CPU-bound tasks (GIL prevents true parallelism)
    
    WHEN TO USE MULTIPROCESSING:
    ✓ CPU-bound tasks (heavy computations, data processing)
    ✓ Need true parallelism across multiple CPU cores
    ✓ Tasks are independent and don't need to share much data
    ✗ Need to share large amounts of data (serialization overhead)
    ✗ Quick, lightweight tasks (process creation overhead)
    
    WHEN TO USE ASYNCIO:
    ✓ I/O-bound tasks with many concurrent operations
    ✓ Network programming (web servers, API clients)
    ✓ Need fine-grained control over task scheduling
    ✓ Working with async libraries (aiohttp, asyncpg)
    ✗ CPU-bound tasks
    ✗ Working with blocking libraries
    
    KEY PRINCIPLES:
    1. Avoid shared mutable state when possible
    2. Use appropriate synchronization primitives (locks, semaphores)
    3. Handle exceptions in concurrent code explicitly
    4. Consider using higher-level abstractions (ThreadPoolExecutor, asyncio.gather)
    5. Profile before optimizing - measure the actual bottleneck
    6. Be aware of the GIL's impact on threading
    7. Use asyncio for I/O-bound tasks with many connections
    8. Use multiprocessing for CPU-bound parallel computation
    
    COMMON PITFALLS:
    • Deadlocks: Circular dependencies in lock acquisition
    • Race conditions: Unsynchronized access to shared data
    • Resource leaks: Not properly closing threads/processes
    • Blocking the event loop: Using blocking calls in async code
    • Excessive context switching: Too many threads/processes
    ============================================================
    """
    print(guidelines)

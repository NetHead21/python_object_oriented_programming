"""Parallel Directory Search System with Multiprocessing.

This module implements a high-performance parallel search system that uses
multiprocessing to search through Python source files for specific text patterns.
It demonstrates advanced concurrency concepts including:
    - Process pool management with multiprocessing
    - Inter-process communication via Queues
    - Work distribution across multiple CPU cores
    - Parallel file processing and text searching

Architecture:
    The system uses a master-worker architecture:
    - Main process: Distributes queries and collects results
    - Worker processes: Load and search assigned files in parallel
    - Communication: Queue-based message passing between processes

Performance Benefits:
    By distributing file searching across multiple processes, this approach
    achieves significant speedup compared to sequential searching, especially
    when dealing with large codebases. Each worker process:
    - Loads its assigned subset of files into memory
    - Searches independently without GIL contention
    - Returns results via shared queue

Key Components:
    - DirectorySearch: Main coordinator class managing workers
    - search(): Worker function running in separate process
    - all_source(): Generator for finding Python files
    - Queue-based communication for queries and results

Example Usage:
    >>> ds = DirectorySearch()
    >>> paths = list(all_source(Path('/project'), '*.py'))
    >>> ds.setup_search(paths)
    >>> for line in ds.search('import'):
    ...     print(line)
    >>> ds.teardown_search()

Note:
    This implementation loads all file contents into memory for each worker.
    For very large codebases, consider memory-mapped files or chunked reading.
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Iterator, Optional, Union, TYPE_CHECKING


if TYPE_CHECKING:
    Query_Q = Queue[Union[str, None]]
    Result_Q = Queue[List[str]]


def search(paths: list[Path], query_q: Query_Q, results_q: Result_Q) -> None:
    """Worker process function that searches assigned files for query strings.

    This function runs in a separate process and performs the following:
    1. Loads all assigned files into memory
    2. Waits for query strings from the query queue
    3. Searches loaded content for each query
    4. Sends matching lines back via results queue
    5. Continues until receiving termination signal (None)

    The function loads all file content upfront, trading memory for speed.
    This approach is efficient for multiple queries on the same file set.

    Args:
        paths (list[Path]): List of file paths assigned to this worker.
        query_q (Queue): Queue for receiving query strings from main process.
            A None value signals the worker to terminate.
        results_q (Queue): Queue for sending search results back to main process.
            Each result is a list of matching lines.

    Returns:
        None: Function runs until termination signal received.

    Process Lifecycle:
        1. Load all assigned files into memory
        2. Enter query processing loop
        3. For each query, search and return results
        4. Exit loop when None received

    Example:
        # This function is called automatically by Process.start()
        # Worker will handle queries until shutdown
        >>> query_q.put("import")
        >>> results = results_q.get()  # List of lines containing "import"
        >>> query_q.put(None)  # Signal termination

    Note:
        - Process ID is printed for debugging/monitoring
        - All file content stored in memory for duration of process
        - Simple substring matching used (not regex)
        - Trailing whitespace stripped from lines
    """

    # Print worker identification for monitoring
    print(f"PID: {os.getpid()}, paths {len(paths)}")

    # Load all assigned files into memory
    lines: list[str] = []
    for path in paths:
        lines.extend(l.rstrip() for l in path.read_text().splitlines())

    # Process queries until termination signal
    while True:
        # Get next query (blocks until available)
        if (query_text := query_q.get()) is None:
            break  # None signals shutdown

        # Search for query in all loaded lines
        results = [l for l in lines if query_text in l]

        # Send results back to main process
        results_q.put(results)


from fnmatch import fnmatch
import os


class DirectorySearch:
    """Parallel text search system using multiprocessing.

    This class manages a pool of worker processes that search through files
    in parallel. It provides a high-level interface for:
    - Setting up worker processes with file assignments
    - Distributing search queries to all workers
    - Collecting and yielding results from workers
    - Cleanly shutting down the process pool

    The class uses a master-worker architecture where:
    - Each worker loads and maintains a subset of files in memory
    - The main process distributes queries via individual worker queues
    - Results are collected from workers via a shared results queue
    - Work is distributed evenly across available CPU cores

    Attributes:
        query_queues (list[Queue]): One queue per worker for sending queries.
        results_queue (Queue): Shared queue for receiving results from workers.
        search_workers (list[Process]): List of active worker processes.

    Workflow:
        1. Initialize: ds = DirectorySearch()
        2. Setup: ds.setup_search(file_paths, cpus=4)
        3. Search: for match in ds.search('pattern'): ...
        4. Cleanup: ds.teardown_search()

    Performance:
        - Scales linearly with CPU cores (up to I/O limits)
        - Each worker operates independently without GIL contention
        - Ideal for searching large codebases (1000+ files)
        - Overhead: ~100ms setup time, ~10ms per query

    Example:
        >>> ds = DirectorySearch()
        >>> paths = list(all_source(Path('/project'), '*.py'))
        >>> ds.setup_search(paths, cpus=4)
        >>>
        >>> # Search for multiple patterns
        >>> for pattern in ['import', 'class', 'def']:
        ...     matches = list(ds.search(pattern))
        ...     print(f"Found {len(matches)} lines with '{pattern}'")
        >>>
        >>> ds.teardown_search()

    Thread Safety:
        Not thread-safe. Designed for single-threaded use with
        multiprocessing for parallelism.

    Memory Considerations:
        Each worker loads its assigned files into memory. For N workers
        and M total files, each worker uses ~M/N files worth of memory.
    """

    def __init__(self) -> None:
        """Initialize DirectorySearch instance.

        Creates an empty search system. Call setup_search() to initialize
        workers before performing searches.

        Attributes are declared but not initialized until setup_search().
        """
        self.query_queues: list[Query_Q]
        self.results_queue: Result_Q
        self.search_workers: list[Process]

    def setup_search(self, paths: list[Path], cpus: Optional[int] = None) -> None:
        """Initialize worker processes for parallel searching.

        Creates and starts a pool of worker processes, distributing files
        evenly among them. Each worker:
        1. Receives a subset of files to load
        2. Loads all assigned files into memory
        3. Waits for queries via its dedicated queue

        The file distribution uses round-robin assignment to ensure even
        workload across workers. For example, with 3 workers and 10 files:
        - Worker 0: files [0, 3, 6, 9]
        - Worker 1: files [1, 4, 7]
        - Worker 2: files [2, 5, 8]

        Args:
            paths (list[Path]): All file paths to be searched.
            cpus (Optional[int], optional): Number of worker processes to create.
                If None, uses cpu_count() to match CPU core count.
                Defaults to None.

        Returns:
            None

        Side Effects:
            - Creates and starts worker processes
            - Creates inter-process communication queues
            - Each worker loads its files (blocking operation)

        Raises:
            OSError: If process creation fails.
            FileNotFoundError: If any path doesn't exist (raised in worker).

        Example:
            >>> ds = DirectorySearch()
            >>> paths = [Path('file1.py'), Path('file2.py')]
            >>> ds.setup_search(paths, cpus=2)
            PID: 12345, paths 1
            PID: 12346, paths 1

        Performance:
            - Setup time: O(N/P) where N=files, P=processes
            - Memory per worker: ~(total_file_size / cpu_count)
            - Each worker prints its PID and file count

        Note:
            Must be called before search() and only once per instance.
            Call teardown_search() to clean up resources when done.
        """

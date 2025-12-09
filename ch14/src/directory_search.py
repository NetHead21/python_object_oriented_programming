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

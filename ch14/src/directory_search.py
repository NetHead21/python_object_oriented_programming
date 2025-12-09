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

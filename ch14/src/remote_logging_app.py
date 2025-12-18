"""Remote Logging Application with Sorting Algorithms.

This module demonstrates remote logging using Python's logging.handlers.SocketHandler
to send log records over TCP to a centralized log server. It implements two sorting
algorithms (BogoSort and GnomeSort) with comprehensive logging to track performance
and execution details.

Key Features:
    - Remote logging via TCP socket to a log server (localhost:18842)
    - Abstract base class (Sorter) for sorting algorithm implementations
    - BogoSort: Brute-force algorithm trying all permutations
    - GnomeSort: Simple comparison-based sorting algorithm
    - Performance tracking with timing measurements
    - Process-specific logging with PID identification

Logging Architecture:
    - Each process creates a logger with name "app_{pid}"
    - Each Sorter instance creates a child logger "app_{pid}.{ClassName}"
    - SocketHandler sends pickled LogRecords to remote server
    - StreamHandler outputs to stderr for local debugging
    - Both handlers configured at INFO level

Use Cases:
    - Demonstrating remote logging in distributed systems
    - Comparing sorting algorithm performance
    - Teaching logging best practices with hierarchical loggers
    - Testing log server implementations (e.g., log_catcher.py)

Network Protocol:
    - Host: localhost (configurable via LOG_HOST)
    - Port: 18842 (configurable via LOG_PORT)
    - Protocol: TCP with pickled LogRecord objects
    - Automatic reconnection on connection failures

Example Usage:
    >>> # Start log server first (e.g., log_catcher.py)
    >>> python remote_logging_app.py
    INFO:app_12345:sorting 10 collections
    INFO:app_12345.GnomeSort:Sorting 7
    INFO:app_12345.GnomeSort:Sorted 7 items, 0.023 ms
    ...
    INFO:app_12345:produced 22 entries, taking 0.045000 s

Sorting Algorithms:
    - BogoSort: O(n×n!) average case - generates random permutations
    - GnomeSort: O(n²) worst case - similar to insertion sort

Performance Notes:
    - BogoSort only practical for very small datasets (n ≤ 10)
    - GnomeSort efficient for small datasets or nearly sorted data
    - Remote logging adds network latency (~1-5ms per log record)

Security Warning:
    - SocketHandler sends pickled objects over network
    - Only use with trusted log servers
    - Consider encrypting connections for sensitive data
"""

from __future__ import annotations
import abc
from itertools import permutations
import logging
import logging.handlers
import os
import random
import time
import sys
from typing import Iterable

logger = logging.getLogger(f"app_{os.getpid()}")

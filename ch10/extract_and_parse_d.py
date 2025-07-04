"""
Directory-Based Log Parser

This module provides functionality to extract and parse warning messages from
multiple log files in a directory. It demonstrates how to process multiple files
using generators and the 'yield from' syntax for efficient memory usage.

Functions:
    file_extract: Extract warnings from multiple log files using generators
    extract_and_parse_d: Process directory of log files and save to CSV
    main: Entry point for standalone execution

Dependencies:
    warnings_filters: Custom module containing warnings_filter function

Author: Python OOP Tutorial
Date: July 2025
"""

import csv
from pathlib import Path
from typing import Iterator, Iterable
from warnings_filters import warnings_filter


def file_extract(path_iter: Iterable[Path]) -> Iterator[tuple[str, ...]]:
    """
    Extract and reformat warning messages from multiple log files.

    Uses generators to efficiently process multiple log files without loading
    all content into memory at once. Demonstrates the 'yield from' syntax for
    delegating to sub-generators.

    Args:
        path_iter (Iterable[Path]): Iterable of Path objects pointing to log files

    Yields:
        tuple[str, ...]: Parsed warning message components (timestamp, level, message)

    Raises:
        FileNotFoundError: If any log file doesn't exist
        PermissionError: If unable to read any log file
        UnicodeDecodeError: If log file contains invalid encoding

    Example:
        >>> log_files = [Path('app1.log'), Path('app2.log')]
        >>> for warning in file_extract(log_files):
        ...     print(f"Warning: {warning[2]}")

    Note:
        This function processes files sequentially and yields warnings as they
        are found, making it memory efficient for large log files.
    """
    for path in path_iter:
        if not path.exists():
            print(f"⚠️  Warning: Log file not found: {path}")
            continue

        try:
            with path.open(encoding="utf-8") as infile:
                # Use 'yield from' to delegate to the warnings_filter generator
                yield from warnings_filter(infile)
        except (PermissionError, UnicodeDecodeError) as e:
            print(f"⚠️  Warning: Could not read {path}: {e}")
            continue

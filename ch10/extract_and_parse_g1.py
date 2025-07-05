"""
Enhanced Generator-Based Log Parser

This module demonstrates an improved approach to extracting and parsing warning
messages from log files using nested generator functions and modern Python features
like the walrus operator (:=).

Functions:
    extract_and_parse_g1: Extract warnings using nested generator function
    main: Entry point for standalone execution

Author: Python OOP Tutorial
Date: July 2025
"""

from pathlib import Path
import re
import csv
from typing import Iterator, Iterable


def extract_and_parse_g1(full_log_path: Path, warning_log_path: Path) -> int:
    """
    Extract warning messages from a log file and save to CSV format using generators.

    Uses a nested generator function to demonstrate encapsulation and modern Python
    features like the walrus operator for efficient pattern matching.

    Args:
        full_log_path (Path): Path to the input log file
        warning_log_path (Path): Path to the output CSV file

    Returns:
        int: Number of warning messages extracted

    Raises:
        FileNotFoundError: If the input log file doesn't exist
        PermissionError: If unable to write to output file
        UnicodeDecodeError: If log file contains invalid encoding
    """
    if not full_log_path.exists():
        raise FileNotFoundError(f"Log file not found: {full_log_path}")

    # Ensure output directory exists
    warning_log_path.parent.mkdir(parents=True, exist_ok=True)

    def warnings_filter(source: Iterable[str]) -> Iterator[tuple[str, str, str]]:
        """
        Filter and reformat warning messages from a log file using generators.

        This nested function demonstrates encapsulation and uses the walrus operator
        for efficient pattern matching and filtering.

        Args:
            source (Iterable[str]): Iterable of log lines

        Yields:
            tuple[str, str, str]: Parsed log components (timestamp, level, message)
        """

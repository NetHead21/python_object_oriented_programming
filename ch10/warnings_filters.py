"""
Warning Log Filter

This module provides a generator-based approach to filter and extract warning messages
from log files. It uses Python generators for memory-efficient processing of large log files.

Functions:
    warnings_filter: Generator function that yields filtered warning messages
    extract_and_parse_3: Extract warnings from log file and save to CSV
    main: Entry point for standalone execution

Author: Python OOP Tutorial
Date: July 2025
"""

import csv
import re
from pathlib import Path
from typing import Iterator, Iterable


def warnings_filter(source: Iterable[str]) -> Iterator[tuple[str, str, str]]:
    """
    Filter and reformat warning messages from a log file using generators.

    This generator function processes log lines one at a time, filtering for
    warning messages and parsing them into structured components. It's memory
    efficient for large log files.

    Args:
        source (Iterable[str]): Iterable of log lines (typically from a file)

    Yields:
        tuple[str, str, str]: Parsed log components (timestamp, level, message)
                             Only yields for lines containing "WARNING"

    Example:
        >>> with open('sample.log') as f:
        ...     for timestamp, level, message in warnings_filter(f):
        ...         print(f"{timestamp}: {message}")

    Note:
        Lines that don't match the expected log format are skipped silently.
        The function assumes log format: "MMM DD, YYYY HH:MM:SS LEVEL message"
    """
    # Fixed pattern to handle single-digit days
    pattern = re.compile(r"(\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2}) (\w+) (.*)")

    for line in source:
        line = line.strip()
        if not line or "WARNING" not in line:
            continue

        match = pattern.match(line)
        if match:
            # Fixed: Properly return the groups as a tuple
            yield match.groups()
        # Skip lines that don't match the pattern


def extract_and_parse_3(full_log_path: Path, warning_log_path: Path) -> None:
    """
    Extract warning messages from log file and save to CSV format.

    Uses the warnings_filter generator to process log files efficiently
    and saves the filtered results to a tab-separated CSV file.

    Args:
        full_log_path (Path): Path to input log file
        warning_log_path (Path): Path to output CSV file

    Raises:
        FileNotFoundError: If input log file doesn't exist
        PermissionError: If unable to write to output file
        UnicodeDecodeError: If log file contains invalid encoding
    """
    if not full_log_path.exists():
        raise FileNotFoundError(f"Log file not found: {full_log_path}")

    with warning_log_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        # Write header row
        writer.writerow(["timestamp", "level", "message"])

        # Open source file with explicit encoding
        with full_log_path.open(encoding="utf-8") as infile:
            warning_filter = warnings_filter(infile)
            for line_groups in warning_filter:
                writer.writerow(line_groups)


def main() -> None:
    """
    Main entry point for the warning log filter.

    Processes 'data/sample.log' and extracts warning messages to 'data/warning.log'
    in CSV format, then displays a sample of the results.

    Raises:
        FileNotFoundError: If 'data/sample.log' doesn't exist
        PermissionError: If unable to write to output directory
    """
    # Define file paths
    full_log_path = Path.cwd() / "data" / "sample.log"
    warning_log_path = Path.cwd() / "data" / "warning.log"

    try:
        print("Processing log file...")
        extract_and_parse_3(full_log_path, warning_log_path)
        print(f"Warning messages extracted to: {warning_log_path}")

        # Display sample results
        if warning_log_path.exists():
            with warning_log_path.open(encoding="utf-8") as f:
                lines = f.readlines()
                print(f"Found {len(lines) - 1} warning messages:")  # -1 for header

                # Show first 5 lines (including header)
                for i, line in enumerate(lines[:5]):
                    print(f"  {line.strip()}")

                if len(lines) > 5:
                    print(f"  ... and {len(lines) - 5} more")

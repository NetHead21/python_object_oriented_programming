"""
Functional Programming Approach to Log Parsing

This module demonstrates a functional programming approach to log parsing using
Python's built-in functional tools: map(), filter(), and lambda functions.
It showcases how to create a processing pipeline using functional programming
paradigms instead of generator expressions.

The functional pipeline:
1. map(pattern.match, source) - Apply regex to all lines
2. filter(None, matches) - Remove non-matching lines
3. map(lambda m: m.groupdict(), matches) - Extract named groups
4. filter(lambda g: g["level"] == "WARNING", groups) - Filter warnings
5. map(datetime_conversion, warnings) - Convert timestamps
6. map(iso_formatting, datetimes) - Format as ISO strings

Functions:
    extract_and_parse_g4: Extract warnings using functional programming
    demonstrate_functional_pipeline: Show functional approach step by step
    main: Entry point for standalone execution
"""

import csv
import re
from pathlib import Path
import datetime


def extract_and_parse_g4(full_log_path: Path, warning_log_path: Path) -> int:
    """
    Extract warning messages using functional programming approach.

    Demonstrates how to use map(), filter(), and lambda functions to create
    a processing pipeline for log data. This approach emphasizes functional
    programming concepts and immutable data transformations.

    Args:
        full_log_path (Path): Path to the input log file
        warning_log_path (Path): Path to the output CSV file

    Returns:
        int: Number of warning messages extracted

    Raises:
        FileNotFoundError: If the input log file doesn't exist
        PermissionError: If unable to write to output file
        UnicodeDecodeError: If log file contains invalid encoding
        ValueError: If datetime parsing fails

    Functional Pipeline:
        1. map() - Apply transformations to all elements
        2. filter() - Select elements matching criteria
        3. lambda - Define inline transformation functions

    Example:
        >>> count = extract_and_parse_g4(Path('app.log'), Path('warnings.csv'))
        >>> print(f"Processed {count} warnings using functional programming")

    Note:
        This approach emphasizes immutable transformations and functional
        composition, making the code more declarative and easier to reason about.
    """
    if not full_log_path.exists():
        raise FileNotFoundError(f"Log file not found: {full_log_path}")

    # Ensure output directory exists
    warning_log_path.parent.mkdir(parents=True, exist_ok=True)
    warning_count = 0

    with warning_log_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        # Write header row
        writer.writerow(["iso_timestamp", "level", "message"])
        # Enhanced regex pattern with flexible day matching
        pattern = re.compile(
            r"(?P<dt>\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2})"
            r"\s+(?P<level>\w+)"
            r"\s+(?P<msg>.*)"
        )

"""
Advanced DateTime Log Parser with Generator Chains

This module demonstrates an advanced log parsing approach using generator chains
with datetime processing. It showcases how to parse timestamps, convert them to
datetime objects, and format them as ISO strings for standardized output.

The generator chain includes:
1. Pattern matching with named groups
2. Dictionary extraction from matches
3. Filtering for WARNING level messages
4. DateTime parsing and conversion
5. ISO format timestamp generation

Functions:
    extract_and_parse_g3: Extract warnings with datetime processing
    demonstrate_datetime_parsing: Show datetime conversion process
    main: Entry point for standalone execution

Author: Python OOP Tutorial
Date: July 2025
"""

import datetime
import csv
import re
from pathlib import Path


def extract_and_parse_g3(full_log_path: Path, warning_log_path: Path) -> int:
    """
    Extract warning messages with advanced datetime processing using generator chains.

    This function demonstrates sophisticated generator chaining with datetime parsing.
    It converts log timestamps to Python datetime objects, then formats them as
    ISO strings for standardized, sortable output.

    Args:
        full_log_path (Path): Path to the input log file
        warning_log_path (Path): Path to the output CSV file

    Returns:
        int: Number of warning messages extracted and processed

    Raises:
        FileNotFoundError: If the input log file doesn't exist
        PermissionError: If unable to write to output file
        UnicodeDecodeError: If log file contains invalid encoding
        ValueError: If datetime parsing fails for any log entry

    Features:
        - Named regex groups for clearer code
        - DateTime parsing and ISO formatting
        - Generator chain for memory efficiency
        - Standardized timestamp output

    Example:
        >>> count = extract_and_parse_g3(Path('app.log'), Path('warnings.csv'))
        >>> print(f"Processed {count} warnings with datetime conversion")

    Output Format:
        ISO timestamp (YYYY-MM-DDTHH:MM:SS), level, message
        Example: 2025-07-05T14:30:45, WARNING, Database connection timeout
    """

    if not full_log_path.exists():
        raise FileNotFoundError(f"Log file not found: {full_log_path}")

    # Ensure output directory exists
    warning_log_path.parent.mkdir(parents=True, exist_ok=True)
    warning_count = 0

    with warning_log_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        # Write header with standardized column names
        writer.writerow(["iso_timestamp", "level", "message"])

        # Enhanced regex pattern with named groups and flexible day matching
        pattern = re.compile(
            r"(?P<dt>\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2})"
            r"\s+(?P<level>\w+)"
            r"\s+(?P<msg>.*)"
        )
        with full_log_path.open(encoding="utf-8") as source:
            # Generator chain with comprehensive processing
            # Stage 1: Pattern matching with named groups
            possible_match_iter = (
                pattern.match(line.strip()) for line in source if line.strip()
            )
            # Stage 2: Extract named groups as dictionaries
            group_iter = (match.groupdict() for match in possible_match_iter if match)
            # Stage 3: Filter for WARNING level messages
            warnings_iter = (
                group for group in group_iter if group.get("level") == "WARNING"
            )
            # Stage 4: Parse datetime and convert to structured tuple
            dt_iter = (
                (
                    datetime.datetime.strptime(g["dt"], "%b %d, %Y %H:%M:%S"),
                    g["level"],
                    g["msg"],
                )
                for g in warnings_iter
            )
            # Stage 5: Format datetime as ISO string for standardized output
            warnings_filter = ((g[0].isoformat(), g[1], g[2]) for g in dt_iter)
            # Process each warning through the generator chain
            for warning_tuple in warnings_filter:
                writer.writerow(warning_tuple)
                warning_count += 1

    return warning_count


def demonstrate_datetime_parsing(full_log_path: Path) -> None:
    """
    Demonstrate the datetime parsing process with detailed output.

    Shows how timestamps are parsed from log format to datetime objects
    and then converted to ISO format for standardized output.

    Args:
        full_log_path (Path): Path to the input log file
    """
    if not full_log_path.exists():
        print(f"❌ Log file not found: {full_log_path}")
        return
    print("🕐 DateTime Parsing Demonstration:")
    print("=" * 50)

    pattern = re.compile(
        r"(?P<dt>\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2})"
        r"\s+(?P<level>\w+)"
        r"\s+(?P<msg>.*)"
    )
    with full_log_path.open(encoding="utf-8") as source:
        # Find first few warning messages for demonstration
        warning_examples = []
        for line in source:
            line = line.strip()
            if not line:
                continue

            match = pattern.match(line)
            if match and match.groupdict().get("level") == "WARNING":
                warning_examples.append(match.groupdict())
                if len(warning_examples) >= 3:
                    break

        if not warning_examples:
            print("   No warning messages found for demonstration")
            return

        print(f"📝 Found {len(warning_examples)} warning examples:")
        for i, example in enumerate(warning_examples, 1):
            print(f"\n   Example {i}:")
            print(
                f"   Original: {example['dt']} {example['level']} {example['msg'][:40]}..."
            )
            # Parse datetime
            try:
                dt_obj = datetime.datetime.strptime(example["dt"], "%b %d, %Y %H:%M:%S")
                iso_string = dt_obj.isoformat()

                print(f"   Parsed datetime: {dt_obj}")
                print(f"   ISO format: {iso_string}")
                print("   Benefits: Sortable, standardized, timezone-ready")

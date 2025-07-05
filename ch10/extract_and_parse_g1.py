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
        # Fixed regex pattern to handle single-digit days
        pattern = re.compile(r"(\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2}) (\w+) (.*)")

        for line in source:
            line = line.strip()
            if not line:
                continue

            # Use walrus operator for efficient pattern matching
            if (match := pattern.match(line)) and match.group(2) == "WARNING":
                yield match.groups()

    warning_count = 0

    # Use proper encoding and newline handling
    with warning_log_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        # Write header row
        writer.writerow(["timestamp", "level", "message"])

        with full_log_path.open(encoding="utf-8") as source:
            for line_groups in warnings_filter(source):
                writer.writerow(line_groups)
                warning_count += 1

    return warning_count


def main() -> None:
    """
    Main entry point for the enhanced warning log filter.

    Processes 'data/sample.log' and extracts warning messages to 'data/warning.log'
    using nested generator functions, then displays results with statistics.
    """

    # Define file paths
    full_log_path = Path.cwd() / "data" / "sample.log"
    warning_log_path = Path.cwd() / "data" / "warning.log"

    try:
        print("Processing log file with nested generator functions...")

        # Extract warnings and get count
        warning_count = extract_and_parse_g1(full_log_path, warning_log_path)

        print("✅ Processing complete!")
        print(f"📁 Input file: {full_log_path}")
        print(f"📄 Output file: {warning_log_path}")
        print(f"🔍 Warning messages found: {warning_count}")

         # Display sample results if any warnings were found
        if warning_count > 0:
            print("\n📋 Sample warning messages:")
            with warning_log_path.open(encoding="utf-8") as f:
                lines = f.readlines()

                # Show first few lines (skip header)
                sample_count = min(5, len(lines) - 1)
                for i, line in enumerate(lines[1 : sample_count + 1], 1):
                    if line.strip():
                        parts = line.strip().split("\t")
                        if len(parts) >= 3:
                            timestamp, level, message = parts[0], parts[1], parts[2]
                            print(f"   {i}. [{timestamp}] {level}: {message[:60]}...")

                if len(lines) > 6:
                    print(f"   ... and {len(lines) - 6} more warning messages")
        else:
            print("   No warning messages found in the log file.")

        # File size information
        if warning_log_path.exists():
            output_size = warning_log_path.stat().st_size
            print(f"📊 Output file size: {output_size:,} bytes")
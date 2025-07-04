"""
Generator-Based Log Parser

This module demonstrates using generator expressions to extract and parse warning
messages from log files. It provides a memory-efficient approach for processing
large log files using Python's generator capabilities.

Functions:
    extract_and_parse_g: Extract warnings using generator expressions
    main: Entry point for standalone execution

Author: Python OOP Tutorial
Date: July 2025
"""

from pathlib import Path
import re
import csv


def extract_and_parse_g(full_log_path: Path, warning_log_path: Path) -> int:
    """
    Extract warning messages from a log file and save to CSV format using generators.

    Uses generator expressions for memory-efficient processing of log files.
    Filters for WARNING level messages and parses them into structured CSV format.

    Args:
        full_log_path (Path): Path to the input log file
        warning_log_path (Path): Path to the output CSV file

    Returns:
        int: Number of warning messages extracted

    Raises:
        FileNotFoundError: If the input log file doesn't exist
        PermissionError: If unable to write to output file
        UnicodeDecodeError: If log file contains invalid encoding

    Example:
        >>> count = extract_and_parse_g(Path('sample.log'), Path('warnings.csv'))
        >>> print(f"Extracted {count} warning messages")
    """
    if not full_log_path.exists():
        raise FileNotFoundError(f"Log file not found: {full_log_path}")

    # Ensure output directory exists
    warning_log_path.parent.mkdir(parents=True, exist_ok=True)

    warning_count = 0

    with warning_log_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        # Write header row
        writer.writerow(["timestamp", "level", "message"])

        # Fixed regex pattern to handle single-digit days
        pattern = re.compile(r"(\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2}) (\w+) (.*)")

        with full_log_path.open(encoding="utf-8") as source:
            # Generator expression for filtering and parsing warning messages
            warnings_generator = (
                match.groups()
                for line in source
                if line.strip() and "WARNING" in line
                for match in [pattern.match(line.strip())]
                if match is not None
            )

            # Process each warning message
            for line_groups in warnings_generator:
                writer.writerow(line_groups)
                warning_count += 1

    return warning_count


def process_log_with_stats(full_log_path: Path, warning_log_path: Path) -> dict:
    """
    Process log file and return detailed statistics.

    Args:
        full_log_path (Path): Path to the input log file
        warning_log_path (Path): Path to the output CSV file

    Returns:
        dict: Statistics about the processing including counts and file info
    """
    if not full_log_path.exists():
        raise FileNotFoundError(f"Log file not found: {full_log_path}")

    stats = {
        "total_lines": 0,
        "warning_lines": 0,
        "parsed_warnings": 0,
        "skipped_lines": 0,
        "file_size": full_log_path.stat().st_size,
    }

    pattern = re.compile(r"(\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2}) (\w+) (.*)")

    with warning_log_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        writer.writerow(["timestamp", "level", "message"])

        with full_log_path.open(encoding="utf-8") as source:
            for line in source:
                stats["total_lines"] += 1
                line = line.strip()

                if not line:
                    continue

                if "WARNING" in line:
                    stats["warning_lines"] += 1
                    match = pattern.match(line)
                    if match:
                        writer.writerow(match.groups())
                        stats["parsed_warnings"] += 1
                    else:
                        stats["skipped_lines"] += 1

    return stats


def main() -> None:
    """
    Main entry point for the generator-based log parser.

    Processes 'data/sample.log' and extracts warning messages to 'data/warning.log'
    using generator expressions, then displays processing statistics and sample results.
    """
    # Define file paths
    full_log_path = Path.cwd() / "data" / "sample.log"
    warning_log_path = Path.cwd() / "data" / "warning.log"

    try:
        print("Processing log file with generator expressions...")

        # Process with detailed statistics
        stats = process_log_with_stats(full_log_path, warning_log_path)

        # Display processing statistics
        print("\n📊 Processing Statistics:")
        print(f"   Total lines processed: {stats['total_lines']:,}")
        print(f"   Warning lines found: {stats['warning_lines']:,}")
        print(f"   Successfully parsed: {stats['parsed_warnings']:,}")
        print(f"   Skipped (format issues): {stats['skipped_lines']:,}")
        print(f"   Input file size: {stats['file_size']:,} bytes")
        print(f"   Output file: {warning_log_path}")

        # Display sample results if any warnings were found
        if stats["parsed_warnings"] > 0:
            print("\n📋 Sample warning messages:")
            with warning_log_path.open(encoding="utf-8") as f:
                lines = f.readlines()

                # Show first few lines (skip header)
                for i, line in enumerate(lines[1:6], 1):
                    if line.strip():
                        parts = line.strip().split("\t")
                        if len(parts) >= 3:
                            timestamp, level, message = parts[0], parts[1], parts[2]
                            print(f"   {i}. [{timestamp}] {level}: {message[:60]}...")

                if len(lines) > 6:
                    print(f"   ... and {len(lines) - 6} more warning messages")
        else:
            print("   No warning messages found in the log file.")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Make sure 'data/sample.log' exists in the current directory")
    except PermissionError as e:
        print(f"❌ Permission error: {e}")
        print("   Check write permissions for the output directory")
    except UnicodeDecodeError as e:
        print(f"❌ Encoding error: {e}")
        print("   The log file may contain invalid UTF-8 characters")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("   Please check the log file format and try again")


if __name__ == "__main__":
    main()

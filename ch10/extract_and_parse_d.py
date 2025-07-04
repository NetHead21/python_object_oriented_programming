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


def extract_and_parse_d(directory: Path, warning_log_path: Path) -> int:
    """
    Extract warning messages from multiple log files in a directory and save to CSV.

    Searches for log files matching the pattern "sample*.log" in the specified
    directory and processes them to extract warning messages into a CSV file.

    Args:
        directory (Path): Directory containing log files to process
        warning_log_path (Path): Path to the output CSV file

    Returns:
        int: Number of warning messages extracted from all files

    Raises:
        FileNotFoundError: If the directory doesn't exist
        PermissionError: If unable to write to output file

    Example:
        >>> count = extract_and_parse_d(Path('logs'), Path('warnings.csv'))
        >>> print(f"Extracted {count} warnings from directory")

    Note:
        The function looks for files matching the pattern "sample*.log".
        If no matching files are found, it will create an empty CSV with headers.
    """

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not directory.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")

    # Ensure output directory exists
    warning_log_path.parent.mkdir(parents=True, exist_ok=True)

    warning_count = 0
    with warning_log_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.writer(target, delimiter="\t")
        # Write header row
        writer.writerow(["timestamp", "level", "message"])

        # Find all log files matching the pattern
        log_files = list(directory.glob("sample*.log"))

        if not log_files:
            print(
                f"⚠️  No log files found matching pattern 'sample*.log' in {directory}"
            )
            return 0

        print(f"📁 Found {len(log_files)} log file(s) to process:")
        for log_file in log_files:
            print(f"   - {log_file.name}")

        # Process all log files and extract warnings
        for line_groups in file_extract(log_files):
            writer.writerow(line_groups)
            warning_count += 1

    return warning_count


def main() -> None:
    """
    Main entry point for the directory-based log parser.

    Processes all log files matching 'sample*.log' in the 'data' directory
    and extracts warning messages to 'data/warning.log' in CSV format.

    Displays processing statistics and sample results.
    """
    # Define directory and output file paths
    log_directory_path = Path.cwd() / "data"
    warning_log_path = log_directory_path / "warning.log"

    try:
        print("🔍 Processing directory of log files...")
        print(f"📂 Looking in directory: {log_directory_path}")

        # Extract warnings from all log files in directory
        warning_count = extract_and_parse_d(log_directory_path, warning_log_path)

        print("\n✅ Processing complete!")
        print(f"📄 Output file: {warning_log_path}")
        print(f"🔍 Total warning messages found: {warning_count}")

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

            # File size information
            output_size = warning_log_path.stat().st_size
            print(f"📊 Output file size: {output_size:,} bytes")
        else:
            print("   No warning messages found in any log files.")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Make sure the 'data' directory exists and contains log files")
    except ValueError as e:
        print(f"❌ Error: {e}")
    except PermissionError as e:
        print(f"❌ Permission error: {e}")
        print("   Check write permissions for the output directory")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure 'warnings_filters.py' exists and is accessible")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("   Please check the log file format and try again")

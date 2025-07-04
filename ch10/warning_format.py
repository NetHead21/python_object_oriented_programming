"""
Warning Log Formatter

This module provides functionality to extract and reformat warning messages from log files.
It implements an iterator-based approach to process log files efficiently and extract only
warning-level messages to a CSV format for further analysis.

The module includes:
- WarningReformat: An iterator class that filters and formats warning messages
- extract_and_parse_2: Function to process log files and save results to CSV
- main: Entry point for standalone execution

Usage:
    python warning_format.py

The script looks for 'data/sample.log' and extracts warning messages to 'data/warning.log'
in tab-separated CSV format.

Author: Python OOP Tutorial
Date: July 2025
"""

import csv
import re
from pathlib import Path
from typing import Iterator, TextIO


class WarningReformat(Iterator[tuple[str, ...]]):
    """
    Iterator to extract and reformat warning messages from a log file.
    
    This class implements the iterator protocol to efficiently process log files
    line by line, filtering for warning messages and parsing them into structured
    components (timestamp, level, message).
    
    Attributes:
        pattern (re.Pattern): Compiled regex pattern to match log line format
        insequence (TextIO): Input file object to read from
    
    Example:
        >>> with open('sample.log', 'r') as f:
        ...     warning_iter = WarningReformat(f)
        ...     for timestamp, level, message in warning_iter:
        ...         print(f"{timestamp}: {message}")
    """

    # Fixed pattern to handle single-digit days
    pattern = re.compile(r"(\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2}) (\w+) (.*)")

    def __init__(self, source: TextIO) -> None:
        """
        Initialize the WarningReformat iterator.
        
        Args:
            source (TextIO): Open file object to read log lines from.
                            Must be opened in text mode with appropriate encoding.
        
        Note:
            The source file object should remain open during iteration.
            The iterator will read from the current position in the file.
        """
        self.insequence: TextIO = source

    def __iter__(self) -> Iterator[tuple[str, ...]]:
        """
        Return the iterator object itself.
        
        Returns:
            Iterator[tuple[str, ...]]: Self reference for iteration protocol
        """
        return self

    def __next__(self) -> tuple[str, ...]:
        """
        Get the next warning message from the log file.
        
        Reads lines from the input file until a warning message is found,
        then parses it using the compiled regex pattern.
        
        Returns:
            tuple[str, ...]: Parsed log components (timestamp, level, message)
                           Example: ('Jul 04, 2025 14:30:45', 'WARNING', 'This is a warning')
        
        Raises:
            StopIteration: When no more warning messages are found in the file
        
        Note:
            This method will skip non-warning lines and continue reading until
            a warning is found or the end of file is reached.
        """
        line = self.insequence.readline()
        # Continue reading until we find a WARNING line or reach end of file
        while line and "WARNING" not in line:
            line = self.insequence.readline()  # Fixed: was missing .readline()

        # If we've reached the end of the file, stop iteration
        if not line:
            raise StopIteration

        # Parse the warning line using regex pattern
        match = self.pattern.match(line.strip())
        if match:
            # Return the parsed components as a tuple
            return match.groups()
        else:
            # If line doesn't match expected format, try next line recursively
            return self.__next__()


def extract_and_parse_2(full_log_path: Path, warning_log_path: Path) -> None:
    """
    Extract and parse warning messages from log file to CSV format.
    
    Reads a log file, filters for warning messages, and saves them to a CSV file
    with tab-separated values. The output includes a header row and parsed
    components of each warning message.
    
    Args:
        full_log_path (Path): Path to the input log file to process.
                             Must exist and be readable.
        warning_log_path (Path): Path to the output CSV file where warning
                                messages will be saved. Will be created or
                                overwritten if it exists.
    
    Returns:
        None: Results are written to the specified output file.
    
    Raises:
        FileNotFoundError: If the input log file doesn't exist
        PermissionError: If unable to write to the output file
        UnicodeDecodeError: If the log file contains invalid UTF-8 characters
    
    Output Format:
        Tab-separated CSV with columns: timestamp, level, message
        Example:
            timestamp	level	message
            Jul 04, 2025 14:30:45	WARNING	This is a warning message
            Jul 04, 2025 14:31:20	WARNING	Another warning occurred
    
    Note:
        The function will process the entire input file and extract only
        lines that contain "WARNING" in them. Multi-line log entries may
        not be handled correctly.
    """
    with warning_log_path.open("w", encoding="utf-8", newline="") as target:
        # Create CSV writer with tab delimiter
        writer = csv.writer(target, delimiter="\t")
        # Write header row for CSV structure
        writer.writerow(["timestamp", "level", "message"])

        # Open source log file and create iterator
        with full_log_path.open(encoding="utf-8") as source:  # Added encoding
            filter_reformat = WarningReformat(source)
            # Iterate through warning messages and write to CSV
            for line_groups in filter_reformat:
                writer.writerow(line_groups)


def main() -> None:
    """
    Main entry point for the warning log formatter.
    
    Configures default file paths and orchestrates the warning extraction process.
    Looks for 'data/sample.log' in the current directory and extracts warning
    messages to 'data/warning.log' in CSV format.
    
    The function will:
    1. Set up input and output file paths
    2. Validate that the input file exists
    3. Process the log file to extract warnings
    4. Display results and sample output
    
    Raises:
        FileNotFoundError: If 'data/sample.log' is not found in the current directory
        PermissionError: If unable to write to the output directory
        
    Output:
        Prints processing status and sample results to stdout.
        Creates 'data/warning.log' file with extracted warning messages.
    
    File Structure Expected:
        current_directory/
        ├── warning_format.py
        └── data/
            ├── sample.log      (input - must exist)
            └── warning.log     (output - will be created)
    
    Example Output:
        Processing log file...
        Warning messages extracted to: /path/to/data/warning.log
        Found 25 warning messages:
          timestamp	level	message
          Jul 04, 2025 14:30:45	WARNING	This is a warning message
          ...
    """
    # Define file paths relative to current directory
    full_log_path = Path.cwd() / "data" / "sample.log"
    warning_log_path = Path.cwd() / "data" / "warning.log"

    # Validate input file exists before processing
    if not full_log_path.exists():
        raise FileNotFoundError(f"Log file not found: {full_log_path}")

    print("Processing log file...")
    extract_and_parse_2(full_log_path, warning_log_path)
    print(f"Warning messages extracted to: {warning_log_path}")

    # Display results summary and sample output
    if warning_log_path.exists():
        with warning_log_path.open(encoding="utf-8") as f:
            lines = f.readlines()
            print(f"Found {len(lines)-1} warning messages:")  # -1 for header
            # Show first 5 lines as sample
            for line in lines[:5]:  # Show first 5 lines
                print(f"  {line.strip()}")
            if len(lines) > 5:
                print(f"  ... and {len(lines)-5} more")


if __name__ == "__main__":
    main()

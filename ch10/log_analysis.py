from pathlib import Path
import re
import csv
import logging
import argparse
import sys

# Set up paths relative to the script location
SCRIPT_DIR = Path(__file__).parent
DEFAULT_LOG_PATH = SCRIPT_DIR / "data" / "sample.log"
DEFAULT_WARNING_PATH = SCRIPT_DIR / "data" / "warning.log"

# Configure logging for this script
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def extract_and_parse_warnings(
    full_log_path: Path, warning_log_path: Path, log_level_filter: str = "WARNING"
) -> int:
    """
    Extract warning messages from a log file and save to CSV format.

    Args:
        full_log_path: Path to the input log file
        warning_log_path: Path to the output CSV file
        log_level_filter: Log level to filter for (default: "WARNING")

    Returns:
        Number of warning messages extracted

    Raises:
        FileNotFoundError: If the input log file doesn't exist
        PermissionError: If unable to write to output file
    """
    if not full_log_path.exists():
        raise FileNotFoundError(f"Log file not found: {full_log_path}")

    # Ensure output directory exists
    warning_log_path.parent.mkdir(parents=True, exist_ok=True)

    # Pattern to match log format: "MMM DD, YYYY HH:MM:SS LEVEL message"
    pattern = re.compile(r"(\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2}) (\w+) (.*)")
    warning_count = 0

    try:
        with warning_log_path.open("w", newline="", encoding="utf-8") as target:
            writer = csv.writer(target, delimiter="\t")
            # Write header
            writer.writerow(["timestamp", "level", "message"])

            with full_log_path.open("r", encoding="utf-8") as source:
                for line_num, line in enumerate(source, 1):
                    line = line.strip()
                    if not line:
                        continue

                    # Check if line contains the specified log level
                    if log_level_filter in line:
                        match = pattern.match(line)
                        if match:
                            timestamp, level, message = match.groups()
                            writer.writerow([timestamp, level, message])
                            warning_count += 1
                        else:
                            logger.warning(
                                f"Line {line_num} doesn't match expected format: {line[:50]}..."
                            )

    except PermissionError as e:
        logger.error(f"Permission denied writing to {warning_log_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing log files: {e}")
        raise

    logger.info(
        f"Extracted {warning_count} {log_level_filter} messages to {warning_log_path}"
    )
    return warning_count


def extract_all_log_levels(full_log_path: Path, output_dir: Path) -> dict[str, int]:
    """
    Extract all log levels from a log file into separate CSV files.

    Args:
        full_log_path: Path to the input log file
        output_dir: Directory to save the CSV files

    Returns:
        Dictionary with log levels as keys and counts as values
    """
    if not full_log_path.exists():
        raise FileNotFoundError(f"Log file not found: {full_log_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    pattern = re.compile(r"(\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2}) (\w+) (.*)")
    log_counts = {}
    writers = {}
    files = {}

    try:
        with full_log_path.open("r", encoding="utf-8") as source:
            for line_num, line in enumerate(source, 1):
                line = line.strip()
                if not line:
                    continue

                match = pattern.match(line)
                if match:
                    timestamp, level, message = match.groups()

                    # Initialize writer for this log level if not exists
                    if level not in writers:
                        output_file = output_dir / f"{level.lower()}_logs.csv"
                        files[level] = output_file.open(
                            "w", newline="", encoding="utf-8"
                        )
                        writers[level] = csv.writer(files[level], delimiter="\t")
                        writers[level].writerow(["timestamp", "level", "message"])
                        log_counts[level] = 0

                    writers[level].writerow([timestamp, level, message])
                    log_counts[level] += 1
                else:
                    logger.warning(
                        f"Line {line_num} doesn't match expected format: {line[:50]}..."
                    )

    finally:
        # Close all open files
        for file in files.values():
            file.close()

    for level, count in log_counts.items():
        logger.info(f"Extracted {count} {level} messages")

    return log_counts


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""

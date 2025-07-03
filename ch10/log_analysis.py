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

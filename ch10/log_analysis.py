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

import sys
from pathlib import Path
from typing import Iterator

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import checksum_writer
import pytest
from unittest.mock import Mock, sentinel

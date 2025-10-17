import sys
from pathlib import Path
from typing import Iterator

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import checksum_writer
import pytest
from unittest.mock import Mock, sentinel


@pytest.fixture
def working_directory(tmp_path: Path) -> Iterator[tuple[Path, Path]]:
    working = tmp_path / "some_directory"
    working.mkdir()
    source_file = working / "data.txt"
    source_file.write_bytes(b"Sample data for checksum testing.")
    checksum = working / "checksum.txt"
    checksum.write_text("data.txt Old_checksum")
    yield source_file, checksum
    # Cleanup is handled by tmp_path fixture
    checksum.unlink(missing_ok=True)
    source_file.unlink(missing_ok=True)

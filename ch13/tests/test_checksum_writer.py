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


@pytest.mark.skipif(sys.version_info < (3, 9), reason="Requires Python 3.9+ features")
def test_checksum(working_directory: tuple[Path, Path]) -> None:
    source_file, old_checksum_path = working_directory
    checksum_writer.checksum(source_file, old_checksum_path)

    # Verify backup file creation
    backup_path = old_checksum_path.with_stem(f"(old) {old_checksum_path.stem}")
    assert backup_path.exists()
    assert old_checksum_path.exists()

    # Verify checksum content
    name, checksum = old_checksum_path.read_text().strip().split()
    assert name == source_file.name
    assert (
        checksum == "5861e7aa80232351e5ada53e36b4f0be98e463758e6f243f5fd55635c8cc8197"
    )


@pytest.fixture
def mock_hashlib(monkeypatch: any) -> Mock:
    mock_hashlib = Mock(sha256=Mock(return_value=sentinel.checksum))
    monkeypatch.setattr(checksum_writer, "hashlib", mock_hashlib)
    return mock_hashlib


def test_file_checksum(mock_hashlib: Mock, tmp_path: Path) -> None:
    source_file = tmp_path / "some_file"
    source_file.write_text("Test content")
    cw = checksum_writer.FileChecksum(source_file)
    assert cw.source == source_file
    assert cw.checksum == sentinel.checksum

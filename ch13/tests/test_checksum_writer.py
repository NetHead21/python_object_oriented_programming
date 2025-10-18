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


# ============================================================================
# Edge Case Tests
# ============================================================================


class TestChecksumEdgeCases:
    """Test edge cases for the checksum function."""

    def test_checksum_empty_file(self, tmp_path: Path) -> None:
        """Test checksum computation for an empty file."""
        source_file = tmp_path / "empty.txt"
        source_file.write_bytes(b"")
        checksum_path = tmp_path / "empty.sha256"

        checksum_writer.checksum(source_file, checksum_path)

        assert checksum_path.exists()
        name, checksum = checksum_path.read_text().strip().split()
        assert name == "empty.txt"
        # SHA-256 of empty string
        assert (
            checksum
            == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        )

    def test_checksum_binary_file(self, tmp_path: Path) -> None:
        """Test checksum computation for binary data."""
        source_file = tmp_path / "binary.bin"
        binary_data = bytes([0, 1, 2, 3, 255, 254, 253, 128])
        source_file.write_bytes(binary_data)
        checksum_path = tmp_path / "binary.sha256"
        checksum_writer.checksum(source_file, checksum_path)

        assert checksum_path.exists()
        content = checksum_path.read_text()
        assert "binary.bin" in content
        assert len(content.strip().split()[1]) == 64  # SHA-256 is 64 hex chars

    def test_checksum_large_file(self, tmp_path: Path) -> None:
        """Test checksum computation for a large file."""
        source_file = tmp_path / "large.dat"
        # Create a 1MB file
        large_data = b"A" * (1024 * 1024)
        source_file.write_bytes(large_data)
        checksum_path = tmp_path / "large.sha256"

        checksum_writer.checksum(source_file, checksum_path)

        assert checksum_path.exists()
        name, checksum = checksum_path.read_text().strip().split()
        assert name == "large.dat"
        assert len(checksum) == 64

    def test_checksum_special_characters_in_filename(self, tmp_path: Path) -> None:
        """Test checksum with special characters in filename."""
        source_file = tmp_path / "file-with_special.chars[123].txt"
        source_file.write_bytes(b"data")
        checksum_path = tmp_path / "special.sha256"

        checksum_writer.checksum(source_file, checksum_path)

        assert checksum_path.exists()
        content = checksum_path.read_text()
        assert "file-with_special.chars[123].txt" in content

    def test_checksum_unicode_content(self, tmp_path: Path) -> None:
        """Test checksum with Unicode content in file."""
        source_file = tmp_path / "unicode.txt"
        source_file.write_text("Hello 世界 🌍 مرحبا", encoding="utf-8")
        checksum_path = tmp_path / "unicode.sha256"

        checksum_writer.checksum(source_file, checksum_path)

        assert checksum_path.exists()
        name, checksum = checksum_path.read_text().strip().split()
        assert name == "unicode.txt"
        assert len(checksum) == 64

    def test_checksum_without_existing_checksum_file(self, tmp_path: Path) -> None:
        """Test checksum when checksum file doesn't exist initially."""
        source_file = tmp_path / "new.txt"
        source_file.write_bytes(b"New content")
        checksum_path = tmp_path / "new.sha256"

        # Ensure checksum file doesn't exist
        assert not checksum_path.exists()

        checksum_writer.checksum(source_file, checksum_path)

        assert checksum_path.exists()
        # No backup should be created
        backup_path = checksum_path.with_stem(f"(old) {checksum_path.stem}")
        assert not backup_path.exists()

    def test_checksum_overwrites_existing_file(self, tmp_path: Path) -> None:
        """Test that checksum overwrites existing checksum file."""
        source_file = tmp_path / "data.txt"
        source_file.write_bytes(b"Original data")
        checksum_path = tmp_path / "data.sha256"
        checksum_path.write_text("data.txt old_checksum_value\n")

        checksum_writer.checksum(source_file, checksum_path)

        # New checksum should be different from "old_checksum_value"
        content = checksum_path.read_text()
        assert "old_checksum_value" not in content

    def test_checksum_backup_preserves_old_content(self, tmp_path: Path) -> None:
        """Test that backup file contains the old checksum."""
        source_file = tmp_path / "data.txt"
        source_file.write_bytes(b"Data")
        checksum_path = tmp_path / "data.sha256"
        old_content = "data.txt old_checksum_12345"
        checksum_path.write_text(old_content)

        checksum_writer.checksum(source_file, checksum_path)

        backup_path = checksum_path.with_stem(f"(old) {checksum_path.stem}")
        assert backup_path.exists()
        assert backup_path.read_text() == old_content

    def test_checksum_multiple_backups(self, tmp_path: Path) -> None:
        """Test that multiple checksum calls create only one backup (overwriting)."""
        source_file = tmp_path / "data.txt"
        source_file.write_bytes(b"Data")
        checksum_path = tmp_path / "data.sha256"

        # First checksum
        checksum_path.write_text("data.txt first_checksum")
        checksum_writer.checksum(source_file, checksum_path)

        backup_path = checksum_path.with_stem(f"(old) {checksum_path.stem}")
        first_backup = backup_path.read_text()

        # Second checksum
        checksum_writer.checksum(source_file, checksum_path)

        # Backup should now contain the previous checksum, not the first one
        second_backup = backup_path.read_text()
        assert second_backup != first_backup
        assert "first_checksum" not in second_backup

    def test_checksum_different_extensions(self, tmp_path: Path) -> None:
        """Test checksum with various file extensions."""
        extensions = [".txt", ".bin", ".dat", ".log", ".json", ".xml", ""]

        for ext in extensions:
            source_file = tmp_path / f"file{ext}"
            source_file.write_bytes(b"test data")
            checksum_path = tmp_path / f"checksum{ext}.sha256"

            checksum_writer.checksum(source_file, checksum_path)

            assert checksum_path.exists()
            name = checksum_path.read_text().strip().split()[0]
            assert name == f"file{ext}"

    def test_checksum_same_content_different_files(self, tmp_path: Path) -> None:
        """Test that files with same content produce the same checksum."""
        content = b"Identical content"

        file1 = tmp_path / "file1.txt"
        file1.write_bytes(content)
        checksum1_path = tmp_path / "file1.sha256"

        file2 = tmp_path / "file2.txt"
        file2.write_bytes(content)
        checksum2_path = tmp_path / "file2.sha256"

        checksum_writer.checksum(file1, checksum1_path)
        checksum_writer.checksum(file2, checksum2_path)

        _, hash1 = checksum1_path.read_text().strip().split()
        _, hash2 = checksum2_path.read_text().strip().split()

        assert hash1 == hash2

    def test_checksum_different_content_different_hashes(self, tmp_path: Path) -> None:
        """Test that files with different content produce different checksums."""
        file1 = tmp_path / "file1.txt"
        file1.write_bytes(b"Content A")
        checksum1_path = tmp_path / "file1.sha256"

        file2 = tmp_path / "file2.txt"
        file2.write_bytes(b"Content B")
        checksum2_path = tmp_path / "file2.sha256"

        checksum_writer.checksum(file1, checksum1_path)
        checksum_writer.checksum(file2, checksum2_path)

        _, hash1 = checksum1_path.read_text().strip().split()
        _, hash2 = checksum2_path.read_text().strip().split()

        assert hash1 != hash2

    def test_checksum_newlines_in_content(self, tmp_path: Path) -> None:
        """Test checksum with various newline types."""
        source_file = tmp_path / "newlines.txt"
        source_file.write_bytes(b"Line1\nLine2\r\nLine3\rLine4")
        checksum_path = tmp_path / "newlines.sha256"

        checksum_writer.checksum(source_file, checksum_path)

        assert checksum_path.exists()
        _, checksum = checksum_path.read_text().strip().split()
        assert len(checksum) == 64

    def test_checksum_format_validation(self, tmp_path: Path) -> None:
        """Test that checksum output format is correct."""
        source_file = tmp_path / "test.txt"
        source_file.write_bytes(b"test")
        checksum_path = tmp_path / "test.sha256"

        checksum_writer.checksum(source_file, checksum_path)

        content = checksum_path.read_text()
        parts = content.strip().split()

        # Should have exactly 2 parts: filename and checksum
        assert len(parts) == 2
        assert parts[0] == "test.txt"
        # Checksum should be 64 hex characters
        assert len(parts[1]) == 64
        assert all(c in "0123456789abcdef" for c in parts[1])
        # Should end with newline
        assert content.endswith("\n")


class TestFileChecksumEdgeCases:
    """Test edge cases for the FileChecksum class."""

    def test_file_checksum_empty_file(self, tmp_path: Path) -> None:
        """Test FileChecksum with empty file."""
        source_file = tmp_path / "empty.txt"
        source_file.write_bytes(b"")

        fc = checksum_writer.FileChecksum(source_file)

        assert fc.source == source_file
        assert (
            fc.checksum.hexdigest()
            == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        )

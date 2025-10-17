"""
Checksum Writer Module - File Integrity Verification

This module provides utilities for computing and storing file checksums using
SHA-256 hashing algorithm. It includes functions and classes for generating
checksums and managing checksum files with backup functionality.

Key Features:
- SHA-256 checksum generation
- Automatic backup of existing checksum files
- Object-oriented checksum management
- Support for file integrity verification

Typical Usage:
    from pathlib import Path

    # Using the function
    source_file = Path('data.tar.gz')
    checksum_file = Path('data.sha256')
    checksum(source_file, checksum_file)

    # Using the class
    file_checksum = FileChecksum(source_file)
    digest = file_checksum.checksum.hexdigest()
"""

from pathlib import Path
import hashlib


def checksum(source: Path, checksum_path: Path) -> None:
    if checksum_path.exists():
        backup = checksum_path.with_stem(f"(old) {checksum_path.stem}")
        backup.write_text(checksum_path.read_text())
    checksum = hashlib.sha256(source.read_bytes())
    checksum_path.write_text(f"{source.name} {checksum.hexdigest()}\n")


class FileChecksum:
    def __init__(self, source: Path) -> None:
        self.source = source
        self.checksum = hashlib.sha256(source.read_bytes())

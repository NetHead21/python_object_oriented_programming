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
    """Generate a SHA-256 checksum for a file and write it to a checksum file.

    This function computes the SHA-256 hash of the source file and writes it
    to the specified checksum file. If the checksum file already exists, it
    creates a backup of the existing file before overwriting it.

    The checksum file format is: "<filename> <hex_digest>"

    Args:
        source (Path): Path to the source file to compute checksum for.
            The file must exist and be readable.
        checksum_path (Path): Path where the checksum will be written.
            If it exists, a backup will be created with "(old)" prefix.

    Returns:
        None

    Raises:
        FileNotFoundError: If the source file does not exist.
        PermissionError: If there are insufficient permissions to read
            the source file or write the checksum file.
        IOError: If there are issues reading or writing files.

    Examples:
        >>> from pathlib import Path
        >>> source = Path('document.pdf')
        >>> checksum_file = Path('document.sha256')
        >>> checksum(source, checksum_file)
        # Creates/updates document.sha256 with the SHA-256 hash

        >>> # If checksum_file exists, a backup is created
        >>> checksum(source, checksum_file)
        # Creates "(old) document.sha256" backup before updating

    Note:
        - The backup file is created by prefixing "(old)" to the stem
        - Each call overwrites the previous backup
        - The entire source file is read into memory for hashing
    """

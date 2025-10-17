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

    if checksum_path.exists():
        backup = checksum_path.with_stem(f"(old) {checksum_path.stem}")
        backup.write_text(checksum_path.read_text())
    checksum = hashlib.sha256(source.read_bytes())
    checksum_path.write_text(f"{source.name} {checksum.hexdigest()}\n")


class FileChecksum:
    """A class for managing file checksums with SHA-256 hashing.

    This class encapsulates the checksum computation for a file, storing
    both the file path and its computed hash. It provides an object-oriented
    interface for working with file checksums.

    The checksum is computed immediately upon initialization by reading the
    entire file into memory and generating its SHA-256 hash.

    Attributes:
        source (Path): Path to the source file.
        checksum (hashlib.sha256): SHA-256 hash object containing the
            computed checksum of the file.

    Examples:
        >>> from pathlib import Path
        >>> file_path = Path('archive.tar.gz')
        >>> fc = FileChecksum(file_path)
        >>> print(f"Checksum: {fc.checksum.hexdigest()}")
        Checksum: a1b2c3d4e5f6...

        >>> # Access the source file information
        >>> print(f"File: {fc.source.name}")
        File: archive.tar.gz

        >>> # Get checksum in different formats
        >>> hex_digest = fc.checksum.hexdigest()
        >>> digest_size = fc.checksum.digest_size
        >>> print(f"Digest size: {digest_size} bytes")
        Digest size: 32 bytes

    Note:
        - The entire file is read into memory during initialization
        - For very large files, consider streaming approaches
        - The checksum object can be used for verification operations

    Raises:
        FileNotFoundError: If the source file does not exist.
        PermissionError: If there are insufficient permissions to read the file.
        IOError: If there are issues reading the file.
    """

    def __init__(self, source: Path) -> None:
        """Initialize FileChecksum with a source file.

        Computes the SHA-256 checksum of the provided file immediately
        upon initialization. The entire file is read into memory for
        hash computation.

        Args:
            source (Path): Path to the file to compute checksum for.
                Must be a valid, readable file path.

        Raises:
            FileNotFoundError: If the source file does not exist.
            PermissionError: If the file cannot be read due to permissions.
            IsADirectoryError: If source points to a directory instead of a file.
            IOError: If there are other I/O errors reading the file.

        Examples:
            >>> from pathlib import Path
            >>> fc = FileChecksum(Path('data.bin'))
            >>> # Checksum is immediately available
            >>> print(fc.checksum.hexdigest()[:16])
            a1b2c3d4e5f6g7h8
        """

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

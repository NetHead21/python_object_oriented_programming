"""Comprehensive test suite for directory_search module.

This test module provides extensive coverage of the directory_search parallel
search system, including:
    - Unit tests for individual functions (search, all_source)
    - Unit tests for DirectorySearch class methods
    - Edge case tests (empty files, Unicode, special chars, long lines)
    - Integration tests with real file I/O and multiprocessing
    - Stress tests for performance and scalability

Test Categories:
    1. Basic functionality tests (3 original tests)
    2. Edge case tests for search() worker function (11 tests)
    3. Edge case tests for all_source() directory walker (10 tests)
    4. Edge case tests for DirectorySearch class (9 tests)
    5. Integration tests with real processes and files (6 tests)
    6. Performance and stress tests (2 tests)

Test Approach:
    - Unit tests use mocks to isolate functionality
    - Integration tests use real multiprocessing and file I/O
    - Edge cases cover Unicode, large data, empty data, special characters
    - Stress tests validate scalability with many files/workers

Fixtures:
    - mock_query_queue: Mocked Queue for query communication
    - mock_result_queue: Mocked Queue for result collection
    - mock_paths: Temporary test files for search operations
    - mock_directory: Temporary directory structure with skip dirs
    - mock_queue: Mocked Queue class for dependency injection
    - mock_process: Mocked Process class for testing setup/teardown
"""

import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pytest import *
from unittest.mock import Mock, sentinel, call
import directory_search


@fixture
def mock_query_queue():
    """Create mock query queue with test query and termination signal.

    Returns:
        Mock: Queue that returns 'xyzzy' then None to simulate search and shutdown.
    """
    return Mock(get=Mock(side_effect=["xyzzy", None]))


@fixture
def mock_result_queue():
    """Create mock result queue for collecting search results.

    Returns:
        Mock: Queue with put() method for result submission.
    """
    return Mock(put=Mock())

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


@fixture
def mock_paths(tmp_path):
    """Create temporary test files for search operations.

    Args:
        tmp_path: pytest fixture providing temporary directory.

    Returns:
        list[Path]: Two test files, one with 'xyzzy' match, one without.
    """

    f1 = tmp_path / "file1"
    f1.write_text("not in file1\n")
    f2 = tmp_path / "file2"
    f2.write_text("file2 contains xyzzy\n")
    return [f1, f2]


def test_search(mock_paths, mock_query_queue, mock_result_queue):
    """Test basic search worker function with file matching.

    Verifies that the search() worker:
    - Loads files and searches for query strings
    - Returns matching lines via result queue
    - Terminates on None signal
    """

    directory_search.search(mock_paths, mock_query_queue, mock_result_queue)
    assert mock_query_queue.get.mock_calls == [call(), call()]
    assert mock_result_queue.put.mock_calls == [call(["file2 contains xyzzy"])]


@fixture
def mock_directory(tmp_path):
    """Create temporary directory with skip directory (.tox) for testing.

    Args:
        tmp_path: pytest fixture providing temporary directory.

    Returns:
        Path: Directory containing file1.py and .tox/file2.py.
    """

    f1 = tmp_path / "file1.py"
    f1.write_text("# file1.py\n")
    d1 = tmp_path / ".tox"
    d1.mkdir()
    f2 = tmp_path / ".tox" / "file2.py"
    f2.write_text("# file2.py\n")
    return tmp_path


def test_all_source(mock_directory):
    """Test that all_source skips excluded directories like .tox.

    Verifies that .tox directory and its contents are excluded from results.
    """

    files = list(directory_search.all_source(mock_directory, "*.py"))
    assert files == [mock_directory / "file1.py"]


@fixture
def mock_queue(monkeypatch):
    """Mock the Queue class for testing DirectorySearch setup.

    Args:
        monkeypatch: pytest fixture for patching imports.

    Returns:
        Mock: Mocked Queue class returning configured queue instances.
    """

    mock_instance = Mock(
        name="mock Queue", put=Mock(), get=Mock(return_value=["line with text"])
    )
    mock_queue_class = Mock(return_value=mock_instance)
    monkeypatch.setattr(directory_search, "Queue", mock_queue_class)
    return mock_queue_class


@fixture
def mock_process(monkeypatch):
    """Mock the Process class for testing DirectorySearch worker management.

    Args:
        monkeypatch: pytest fixture for patching imports.

    Returns:
        Mock: Mocked Process class with start() and join() methods.
    """

    mock_instance = Mock(name="mock Process", start=Mock(), join=Mock())
    mock_process_class = Mock(return_value=mock_instance)
    monkeypatch.setattr(directory_search, "Process", mock_process_class)
    return mock_process_class


def test_directory_search(mock_queue, mock_process, mock_paths):
    """Test DirectorySearch class with full lifecycle: setup, search, teardown.

    Verifies:
    - Proper initialization of queues and workers
    - Correct file distribution across workers (round-robin)
    - Query distribution to all workers
    - Result collection from workers
    - Clean shutdown with termination signals
    """

    ds_instance = directory_search.DirectorySearch()
    ds_instance.setup_search(mock_paths, cpus=2)

    assert mock_queue.mock_calls == [call(), call(), call()]
    assert mock_process.mock_calls == [
        call(
            target=directory_search.search,
            args=(mock_paths[0::2], mock_queue.return_value, mock_queue.return_value),
        ),
        call(
            target=directory_search.search,
            args=(mock_paths[1::2], mock_queue.return_value, mock_queue.return_value),
        ),
    ]
    assert mock_process.return_value.start.mock_calls == [call(), call()]
    assert ds_instance.query_queues == [
        mock_queue.return_value,
        mock_queue.return_value,
    ]
    assert ds_instance.results_queue == mock_queue.return_value
    assert ds_instance.search_workers == [
        mock_process.return_value,
        mock_process.return_value,
    ]

    result = list(ds_instance.search("text"))

    assert result == ["line with text", "line with text"]
    assert mock_queue.return_value.put.mock_calls == [call("text"), call("text")]
    assert mock_queue.return_value.get.mock_calls == [call(), call()]

    ds_instance.teardown_search()
    assert mock_queue.return_value.put.mock_calls == [
        call("text"),
        call("text"),
        call(None),
        call(None),
    ]
    assert mock_process.return_value.join.mock_calls == [call(), call()]


# ============================================================================
# Additional Comprehensive Tests with Edge Cases
# ============================================================================


# Edge Case Tests for search() function
# ============================================================================


def test_search_empty_file(tmp_path, mock_query_queue, mock_result_queue):
    """Test search worker handles empty files gracefully.

    Verifies that searching an empty file returns empty results without errors.
    """

    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    directory_search.search([empty_file], mock_query_queue, mock_result_queue)

    assert mock_result_queue.put.mock_calls == [call([])]


def test_search_no_matches(tmp_path, mock_result_queue):
    """Test search returns empty list when no lines match the query.

    Verifies correct behavior when search pattern not found in any lines.
    """

    file1 = tmp_path / "file1.txt"
    file1.write_text("hello\nworld\n")

    mock_queue = Mock(get=Mock(side_effect=["xyz", None]))
    directory_search.search([file1], mock_queue, mock_result_queue)

    assert mock_result_queue.put.mock_calls == [call([])]


def test_search_all_lines_match(tmp_path, mock_result_queue):
    """Test search returns all lines when every line matches the query.

    Verifies that search correctly identifies when all lines contain the pattern.
    """

    file1 = tmp_path / "file1.txt"
    file1.write_text("test line 1\ntest line 2\ntest line 3\n")

    mock_queue = Mock(get=Mock(side_effect=["test", None]))
    directory_search.search([file1], mock_queue, mock_result_queue)

    assert mock_result_queue.put.mock_calls == [
        call(["test line 1", "test line 2", "test line 3"])
    ]


def test_search_multiple_queries(tmp_path, mock_result_queue):
    """Test worker processes multiple queries sequentially before termination.

    Verifies that workers can handle multiple search queries in sequence,
    returning appropriate results for each query.
    """

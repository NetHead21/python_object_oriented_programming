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

    file1 = tmp_path / "file1.txt"
    file1.write_text("import os\nclass MyClass\ndef my_function\n")

    mock_queue = Mock(get=Mock(side_effect=["import", "class", "def", None]))
    directory_search.search([file1], mock_queue, mock_result_queue)

    assert mock_result_queue.put.mock_calls == [
        call(["import os"]),
        call(["class MyClass"]),
        call(["def my_function"]),
    ]


def test_search_case_sensitive(tmp_path, mock_result_queue):
    """Test that search performs case-sensitive matching.

    Verifies 'import' only matches lowercase 'import', not 'Import' or 'IMPORT'.
    """

    file1 = tmp_path / "file1.txt"
    file1.write_text("Import os\nimport sys\nIMPORT json\n")

    mock_queue = Mock(get=Mock(side_effect=["import", None]))
    directory_search.search([file1], mock_queue, mock_result_queue)

    assert mock_result_queue.put.mock_calls == [call(["import sys"])]


def test_search_unicode_content(tmp_path, mock_result_queue):
    """Test search handles Unicode characters correctly (Chinese, Cyrillic, emoji).

    Verifies that search works with multi-byte characters including:
    - Chinese characters (世界)
    - Cyrillic characters (мир)
    - Emoji (🎉)
    """

    file1 = tmp_path / "file1.txt"
    file1.write_text("Hello 世界\nПривет мир\n日本語\némojis 🎉🎊\n")

    mock_queue = Mock(get=Mock(side_effect=["世界", "мир", "🎉", None]))
    directory_search.search([file1], mock_queue, mock_result_queue)

    assert mock_result_queue.put.mock_calls == [
        call(["Hello 世界"]),
        call(["Привет мир"]),
        call(["émojis 🎉🎊"]),
    ]


def test_search_special_characters(tmp_path, mock_result_queue):
    """Test search treats special characters as literals, not regex patterns.

    Verifies literal matching for $, [], (), .* and other regex metacharacters.
    Search uses substring matching, not regular expressions.
    """

    file1 = tmp_path / "file1.txt"
    file1.write_text("$variable = 10\n[bracket]\n(parenthesis)\n.*regex.*\n")

    mock_queue = Mock(get=Mock(side_effect=["$variable", "[bracket]", ".*regex", None]))
    directory_search.search([file1], mock_queue, mock_result_queue)

    assert mock_result_queue.put.mock_calls == [
        call(["$variable = 10"]),
        call(["[bracket]"]),
        call([".*regex.*"]),
    ]


def test_search_long_lines(tmp_path, mock_result_queue):
    """Test search handles very long lines (20,000+ characters) efficiently.

    Verifies that search can process and return extremely long lines without
    truncation or performance issues.
    """

    file1 = tmp_path / "file1.txt"
    long_line = "x" * 10000 + " target " + "y" * 10000
    file1.write_text(f"{long_line}\nshort line\n")

    mock_queue = Mock(get=Mock(side_effect=["target", None]))
    directory_search.search([file1], mock_queue, mock_result_queue)

    results = mock_result_queue.put.mock_calls[0][1][0]
    assert len(results) == 1
    assert "target" in results[0]
    assert len(results[0]) > 20000


def test_search_whitespace_handling(tmp_path, mock_result_queue):
    """Test that trailing whitespace (spaces and tabs) is stripped from lines.

    Verifies rstrip() behavior removes trailing whitespace while preserving
    leading whitespace and mid-line spacing.
    """

    file1 = tmp_path / "file1.txt"
    file1.write_text("line with spaces   \nline with tabs\t\t\nline with both  \t  \n")

    mock_queue = Mock(get=Mock(side_effect=["line", None]))
    directory_search.search([file1], mock_queue, mock_result_queue)

    results = mock_result_queue.put.mock_calls[0][1][0]
    assert results == [
        "line with spaces",
        "line with tabs",
        "line with both",
    ]


def test_search_multiple_files(tmp_path, mock_result_queue):
    """Test worker searches across multiple assigned files and aggregates results.

    Verifies that workers load and search all assigned files, combining
    matches from all sources.
    """

    file1 = tmp_path / "file1.txt"
    file1.write_text("import os\n")
    file2 = tmp_path / "file2.txt"
    file2.write_text("import sys\n")
    file3 = tmp_path / "file3.txt"
    file3.write_text("no match\n")

    mock_queue = Mock(get=Mock(side_effect=["import", None]))
    directory_search.search([file1, file2, file3], mock_queue, mock_result_queue)

    results = mock_result_queue.put.mock_calls[0][1][0]
    assert len(results) == 2
    assert "import os" in results
    assert "import sys" in results


def test_search_partial_match(tmp_path, mock_result_queue):
    """Test that search finds partial/substring matches within lines.

    Verifies 'import' matches 'import os', 'import_helper', and 'important'.
    Demonstrates substring matching behavior.
    """

    file1 = tmp_path / "file1.txt"
    file1.write_text("import os\nfrom import_helper import x\nimportant note\n")

    mock_queue = Mock(get=Mock(side_effect=["import", None]))
    directory_search.search([file1], mock_queue, mock_result_queue)

    results = mock_result_queue.put.mock_calls[0][1][0]
    assert len(results) == 3
    assert "import os" in results
    assert "from import_helper import x" in results
    assert "important note" in results


# Edge Case Tests for all_source() function
# ============================================================================


def test_all_source_empty_directory(tmp_path):
    """Test all_source returns empty list for empty directory.

    Verifies graceful handling when no files exist in target directory.
    """

    files = list(directory_search.all_source(tmp_path, "*.py"))
    assert files == []


def test_all_source_no_matching_files(tmp_path):
    """Test all_source returns empty list when no files match the pattern.

    Verifies pattern filtering works correctly when files exist but don't
    match the specified pattern.
    """

    (tmp_path / "file.txt").write_text("content")
    (tmp_path / "file.md").write_text("content")

    files = list(directory_search.all_source(tmp_path, "*.py"))
    assert files == []


def test_all_source_nested_directories(tmp_path):
    """Test all_source recursively finds files in deeply nested directories.

    Verifies recursive traversal through multiple directory levels,
    finding files at each level.
    """

    (tmp_path / "level1").mkdir()
    (tmp_path / "level1" / "level2").mkdir()
    (tmp_path / "level1" / "level2" / "level3").mkdir()

    (tmp_path / "root.py").write_text("# root")
    (tmp_path / "level1" / "l1.py").write_text("# l1")
    (tmp_path / "level1" / "level2" / "l2.py").write_text("# l2")
    (tmp_path / "level1" / "level2" / "level3" / "l3.py").write_text("# l3")

    files = list(directory_search.all_source(tmp_path, "*.py"))
    assert len(files) == 4
    assert tmp_path / "root.py" in files
    assert tmp_path / "level1" / "l1.py" in files
    assert tmp_path / "level1" / "level2" / "l2.py" in files
    assert tmp_path / "level1" / "level2" / "level3" / "l3.py" in files


def test_all_source_skip_tox_directory(tmp_path):
    """Test that .tox directory and all subdirectories are excluded.
    Verifies .tox exclusion prevents descending into tox virtual environments.
    """

    (tmp_path / ".tox").mkdir()
    (tmp_path / ".tox" / "env").mkdir()
    (tmp_path / "normal.py").write_text("# normal")
    (tmp_path / ".tox" / "skip.py").write_text("# skip")
    (tmp_path / ".tox" / "env" / "skip2.py").write_text("# skip2")

    files = list(directory_search.all_source(tmp_path, "*.py"))
    assert files == [tmp_path / "normal.py"]


def test_all_source_skip_mypy_cache_directory(tmp_path):
    """Test that .mypy_cache directory is excluded from search.

    Verifies exclusion of mypy type checker cache directories.
    """

    (tmp_path / ".mypy_cache").mkdir()
    (tmp_path / "normal.py").write_text("# normal")
    (tmp_path / ".mypy_cache" / "skip.py").write_text("# skip")

    files = list(directory_search.all_source(tmp_path, "*.py"))
    assert files == [tmp_path / "normal.py"]


def test_all_source_skip_pycache_directory(tmp_path):
    """Test that __pycache__ directory is excluded from search.

    Verifies exclusion of Python bytecode cache directories.
    """

    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "normal.py").write_text("# normal")
    (tmp_path / "__pycache__" / "skip.pyc").write_text("# skip")

    files = list(directory_search.all_source(tmp_path, "*.py"))
    assert files == [tmp_path / "normal.py"]


def test_all_source_skip_idea_directory(tmp_path):
    """Test that .idea directory is excluded from search.

    Verifies exclusion of PyCharm/IntelliJ IDE configuration directories.
    """

    (tmp_path / ".idea").mkdir()
    (tmp_path / "normal.py").write_text("# normal")
    (tmp_path / ".idea" / "workspace.xml").write_text("# skip")

    files = list(directory_search.all_source(tmp_path, "*.py"))
    assert files == [tmp_path / "normal.py"]


def test_all_source_multiple_skip_directories(tmp_path):
    """Test that all configured skip directories are excluded simultaneously.

    Verifies that .tox, .mypy_cache, __pycache__, and .idea are all
    excluded while normal directories are included.
    """

    (tmp_path / ".tox").mkdir()
    (tmp_path / ".mypy_cache").mkdir()
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / ".idea").mkdir()
    (tmp_path / "src").mkdir()

    (tmp_path / "normal.py").write_text("# normal")
    (tmp_path / "src" / "app.py").write_text("# app")
    (tmp_path / ".tox" / "skip1.py").write_text("# skip1")
    (tmp_path / ".mypy_cache" / "skip2.py").write_text("# skip2")
    (tmp_path / "__pycache__" / "skip3.py").write_text("# skip3")
    (tmp_path / ".idea" / "skip4.py").write_text("# skip4")

    files = list(directory_search.all_source(tmp_path, "*.py"))
    assert len(files) == 2
    assert tmp_path / "normal.py" in files
    assert tmp_path / "src" / "app.py" in files


def test_all_source_different_patterns(tmp_path):
    """Test all_source with various glob patterns (*.py, *.txt, test_*.py).

    Verifies pattern matching works correctly for different file extensions
    and filename patterns.
    """

    (tmp_path / "file.py").write_text("# py")
    (tmp_path / "file.txt").write_text("# txt")
    (tmp_path / "file.md").write_text("# md")
    (tmp_path / "test_file.py").write_text("# test")

    py_files = list(directory_search.all_source(tmp_path, "*.py"))
    txt_files = list(directory_search.all_source(tmp_path, "*.txt"))
    test_files = list(directory_search.all_source(tmp_path, "test_*.py"))

    assert len(py_files) == 2
    assert len(txt_files) == 1
    assert len(test_files) == 1


def test_all_source_no_extension(tmp_path):
    """Test all_source can match files without extensions (Makefile, README).

    Verifies that exact filename matching works for extensionless files.
    """

    (tmp_path / "Makefile").write_text("# makefile")
    (tmp_path / "README").write_text("# readme")
    (tmp_path / "file.py").write_text("# py")

    files = list(directory_search.all_source(tmp_path, "Makefile"))
    assert len(files) == 1
    assert tmp_path / "Makefile" in files


# Edge Case Tests for DirectorySearch class
# ============================================================================


def test_directory_search_single_cpu(mock_queue, mock_process, mock_paths):
    """Test DirectorySearch with cpus=1 creates single worker.

    Verifies that single-CPU configuration works correctly.
    """

    ds = directory_search.DirectorySearch()
    ds.setup_search(mock_paths, cpus=1)

    assert len(ds.query_queues) == 1
    assert len(ds.search_workers) == 1


def test_directory_search_many_cpus(mock_queue, mock_process, mock_paths):
    """Test DirectorySearch creates workers even when CPUs exceed file count.

    Verifies that requesting 10 workers with only 2 files creates all 10 workers
    (some will have no files to search).
    """

    ds = directory_search.DirectorySearch()
    ds.setup_search(mock_paths, cpus=10)

    # Should create 10 workers even with only 2 files
    assert len(ds.query_queues) == 10
    assert len(ds.search_workers) == 10


def test_directory_search_default_cpus(
    mock_queue, mock_process, mock_paths, monkeypatch
):
    """Test DirectorySearch uses cpu_count when cpus=None."""

    mock_cpu_count = Mock(return_value=8)
    monkeypatch.setattr(directory_search, "cpu_count", mock_cpu_count)

    ds = directory_search.DirectorySearch()
    ds.setup_search(mock_paths, cpus=None)

    mock_cpu_count.assert_called_once()
    assert len(ds.query_queues) == 8


def test_directory_search_empty_file_list(mock_queue, mock_process):
    """Test DirectorySearch handles empty file list gracefully.

    Verifies that workers are created even with no files (they simply wait
    for queries with no content to search).
    """

    ds = directory_search.DirectorySearch()
    ds.setup_search([], cpus=2)

    # Should still create workers, they just have no files
    assert len(ds.query_queues) == 2
    assert len(ds.search_workers) == 2


def test_directory_search_no_results(mock_queue, mock_process, mock_paths):
    """Test search returns empty iterator when no matches found.

    Verifies correct behavior when search pattern doesn't match any content.
    """

    mock_queue_instance = Mock(
        put=Mock(),
        get=Mock(return_value=[]),  # Empty results
    )
    mock_queue.return_value = mock_queue_instance

    ds = directory_search.DirectorySearch()
    ds.setup_search(mock_paths, cpus=2)
    result = list(ds.search("nonexistent"))

    assert result == []


def test_directory_search_multiple_searches(mock_queue, mock_process, mock_paths):
    """Test DirectorySearch can execute multiple searches on same file set.

    Verifies that workers can process multiple different queries sequentially,
    leveraging pre-loaded file content for efficiency.
    """

    call_count = [0]

    def get_side_effect():
        call_count[0] += 1
        if call_count[0] <= 2:
            return ["result1"]
        elif call_count[0] <= 4:
            return ["result2"]
        else:
            return ["result3"]

    mock_queue_instance = Mock(put=Mock(), get=Mock(side_effect=get_side_effect))
    mock_queue.return_value = mock_queue_instance

    ds = directory_search.DirectorySearch()
    ds.setup_search(mock_paths, cpus=2)

    result1 = list(ds.search("query1"))
    result2 = list(ds.search("query2"))
    result3 = list(ds.search("query3"))

    assert result1 == ["result1", "result1"]
    assert result2 == ["result2", "result2"]
    assert result3 == ["result3", "result3"]


def test_directory_search_large_result_set(mock_queue, mock_process, mock_paths):
    """Test search handles large result sets (1000+ lines per worker).

    Verifies that large numbers of matching lines are collected and yielded
    correctly without truncation or memory issues.
    """

    large_results = [f"line {i}" for i in range(1000)]
    mock_queue_instance = Mock(put=Mock(), get=Mock(return_value=large_results))
    mock_queue.return_value = mock_queue_instance

    ds = directory_search.DirectorySearch()
    ds.setup_search(mock_paths, cpus=2)
    result = list(ds.search("target"))

    assert len(result) == 2000  # 1000 from each of 2 workers
    assert result[:1000] == large_results
    assert result[1000:] == large_results


def test_directory_search_work_distribution(mock_queue, mock_process):
    """Test round-robin file distribution ensures balanced workload.

    Verifies that 10 files distributed across 3 workers results in:
    Worker 0: 4 files (indices 0,3,6,9)
    Worker 1: 3 files (indices 1,4,7)
    Worker 2: 3 files (indices 2,5,8)
    """

    files = [Mock() for _ in range(10)]

    ds = directory_search.DirectorySearch()
    ds.setup_search(files, cpus=3)

    # Round-robin: [0,3,6,9], [1,4,7], [2,5,8]
    assert len(worker_0_files) == 4  # indices 0, 3, 6, 9
    assert len(worker_1_files) == 3  # indices 1, 4, 7
    assert len(worker_2_files) == 3  # indices 2, 5, 8


def test_directory_search_teardown_idempotent(mock_queue, mock_process, mock_paths):
    """Test teardown_search is idempotent and safe to call multiple times.

    Verifies that calling teardown multiple times doesn't raise errors
    (though it may send extra termination signals).
    """

    ds = directory_search.DirectorySearch()
    ds.setup_search(mock_paths, cpus=2)

    ds.teardown_search()
    ds.teardown_search()  # Should not raise error

    # Should have sent None twice per worker
    assert mock_queue.return_value.put.mock_calls.count(call(None)) == 4


# Integration Tests
# ============================================================================


def test_full_integration_real_files(tmp_path):
    """Full integration test with real processes, queues, and file I/O.

    Tests complete workflow:
    1. Create real Python files with various content
    2. Use all_source to find files
    3. Setup real worker processes
    4. Execute multiple searches
    5. Verify results match expected patterns
    6. Clean shutdown
    """

    # Create test files
    (tmp_path / "file1.py").write_text("import os\nclass MyClass:\n    pass\n")
    (tmp_path / "file2.py").write_text("def my_function():\n    import sys\n")
    (tmp_path / "file3.py").write_text("# Just a comment\n")

    paths = list(directory_search.all_source(tmp_path, "*.py"))
    assert len(paths) == 3

    ds = directory_search.DirectorySearch()
    ds.setup_search(paths, cpus=2)

    # Search for 'import'
    import_results = list(ds.search("import"))
    assert len(import_results) == 2
    assert any("import os" in r for r in import_results)
    assert any("import sys" in r for r in import_results)

    # Search for 'class'
    class_results = list(ds.search("class"))
    assert len(class_results) == 1
    assert "class MyClass:" in class_results[0]

    # Search for 'def'
    def_results = list(ds.search("def"))
    assert len(def_results) == 1
    assert "def my_function():" in def_results[0]

    ds.teardown_search()

    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "__pycache__").mkdir()

    (tmp_path / "main.py").write_text("import main_module\n")
    (tmp_path / "src" / "app.py").write_text("import app_module\n")
    (tmp_path / "tests" / "test_app.py").write_text("import unittest\n")
    (tmp_path / "__pycache__" / "cache.py").write_text("import cache\n")

    paths = list(directory_search.all_source(tmp_path, "*.py"))
    assert len(paths) == 3  # Excludes __pycache__

    ds = directory_search.DirectorySearch()
    ds.setup_search(paths, cpus=2)

    results = list(ds.search("import"))
    assert len(results) == 3

    ds.teardown_search()


def test_integration_unicode_and_special_chars(tmp_path):
    """Integration test with real Unicode content in files.

    Tests end-to-end search with:
    - Chinese characters (中文字符)
    - Emoji (🎉)
    - Cyrillic (Привет мир)
    - Accented characters (Tëst)
    """

    content = """# -*- coding: utf-8 -*-
    import os
    # Comment with 中文字符
    class Tëst:
        '''Docstring with émojis 🎉'''
        def __init__(self):
            self.data = "Привет мир"
    """

    (tmp_path / "unicode.py").write_text(content)

    paths = list(directory_search.all_source(tmp_path, "*.py"))
    ds = directory_search.DirectorySearch()
    ds.setup_search(paths, cpus=1)

    # Search for various patterns
    assert len(list(ds.search("中文"))) == 1
    assert len(list(ds.search("🎉"))) == 1
    assert len(list(ds.search("Привет"))) == 1
    assert len(list(ds.search("Tëst"))) == 1

    ds.teardown_search()


def test_integration_large_file(tmp_path):
    """Integration test with large file (5000 lines).

    Verifies that search handles large files efficiently and returns
    all matching lines.
    """

    lines = [f"line {i} with target keyword\n" for i in range(5000)]
    large_content = "".join(lines)
    (tmp_path / "large.py").write_text(large_content)

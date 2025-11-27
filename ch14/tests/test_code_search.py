import ast
import sys
from pathlib import Path
from pytest import fixture, mark, raises
from unittest.mock import MagicMock, Mock, sentinel, call


# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import code_search


def test_import_result(tmp_path):
    i1 = code_search.ImportResult(tmp_path, {"math"})
    assert not i1.focus
    i2 = code_search.ImportResult(tmp_path, {"math", "typing"})
    assert i2.focus


@fixture
def mock_directory(tmp_path):
    f1 = tmp_path / "file1.py"
    f1.write_text("# file1.py\n")
    d1 = tmp_path / ".tox"
    d1.mkdir()
    f2 = tmp_path / ".tox" / "file2.py"
    f2.write_text("# file2.py\n")
    return tmp_path


def test_all_source(mock_directory):
    files = list(code_search.all_source(mock_directory, "*.py"))
    assert files == [mock_directory / "file1.py"]


@fixture
def mock_code_1(tmp_path):
    source = tmp_path / "code_1.py"
    source.write_text("import math\nprint(math.pi)\n")
    return source


@fixture
def mock_code_2(tmp_path):
    source = tmp_path / "code_2.py"
    source.write_text("import math\nfrom typing import Callable\nprint(math.pi)\n")
    return source


def test_no_typing(mock_code_1):
    actual = code_search.find_imports(mock_code_1)
    assert actual == code_search.ImportResult(mock_code_1, {"math"})


def test_typing(mock_code_2):
    actual = code_search.find_imports(mock_code_2)
    assert actual == code_search.ImportResult(mock_code_2, {"math", "typing"})


@fixture
def mock_futures_pool(tmp_path, monkeypatch):
    future = Mock(
        result=Mock(
            return_value=code_search.ImportResult(tmp_path / "code.py", {"typing"})
        )
    )
    context = MagicMock(submit=Mock(return_value=future))
    pool = MagicMock(__enter__=Mock(return_value=context))
    pool_class = Mock(return_value=pool)
    monkeypatch.setattr(code_search.futures, "ThreadPoolExecutor", pool_class)
    as_completed = Mock(side_effect=lambda futures: futures)
    monkeypatch.setattr(code_search.futures, "as_completed", as_completed)
    return pool_class


@fixture
def mock_all_source(tmp_path, monkeypatch):
    paths = [tmp_path / "file1.py"]
    function = Mock(return_value=paths)
    monkeypatch.setattr(code_search, "all_source", function)
    return paths


@fixture
def mock_time(monkeypatch):
    time = Mock(perf_counter=Mock(side_effect=[0.0, 0.42]))
    monkeypatch.setattr(code_search, "time", time)
    return time


def test_main(
    mock_all_source, mock_futures_pool, mock_time, tmp_path, capsys, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    code_search.main(tmp_path)
    assert mock_futures_pool.mock_calls == [call(24)]
    context = mock_futures_pool.return_value.__enter__.return_value
    assert context.submit.mock_calls == [
        call(code_search.find_imports, tmp_path / "file1.py")
    ]
    future = context.submit.return_value
    assert future.result.mock_calls == [call()]
    out, err = capsys.readouterr()
    target_path = "code.py"
    assert out.splitlines() == [
        "",
        str(tmp_path),
        f"-> {str(target_path)} {{'typing'}}",
        f"Searched 1 files in {str(tmp_path)} (420.000ms/file)",
    ]


# ============================================================================
# ADDITIONAL EDGE CASES AND COMPREHENSIVE TESTS
# ============================================================================


class TestImportResult:
    """Comprehensive tests for ImportResult class."""

    def test_import_result_with_empty_imports(self, tmp_path):
        """Test ImportResult with no imports."""
        result = code_search.ImportResult(tmp_path, set())
        assert result.path == tmp_path
        assert result.imports == set()
        assert not result.focus

    def test_import_result_with_multiple_imports(self, tmp_path):
        """Test ImportResult with multiple imports including typing."""
        imports = {"os", "sys", "typing", "pathlib", "json"}
        result = code_search.ImportResult(tmp_path, imports)
        assert result.imports == imports
        assert result.focus

    def test_import_result_equality(self, tmp_path):
        """Test equality of ImportResult instances."""
        result1 = code_search.ImportResult(tmp_path, {"os", "sys"})
        result2 = code_search.ImportResult(tmp_path, {"os", "sys"})
        assert result1 == result2

    def test_import_result_ordering(self, tmp_path):
        """Test that ImportResults can be sorted by path."""
        result1 = code_search.ImportResult(tmp_path / "a.py", {"os"})
        result2 = code_search.ImportResult(tmp_path / "b.py", {"sys"})
        result3 = code_search.ImportResult(tmp_path / "c.py", {"json"})

        sorted_results = sorted([result3, result1, result2])
        assert sorted_results == [result1, result2, result3]

    def test_import_result_focus_case_sensitive(self, tmp_path):
        """Test that focus check is case-sensitive."""
        result = code_search.ImportResult(tmp_path, {"Typing", "TYPING"})
        assert not result.focus  # Should not match "typing"


class TestImportVisitor:
    """Comprehensive tests for ImportVisitor class."""

    def test_visitor_empty_file(self):
        """Test visitor with empty Python file."""
        tree = ast.parse("")
        visitor = code_search.ImportVisitor()
        visitor.visit(tree)
        assert visitor.imports == set()

    def test_visitor_single_import(self):
        """Test visitor with single import statement."""
        tree = ast.parse("import os")
        visitor = code_search.ImportVisitor()
        visitor.visit(tree)
        assert visitor.imports == {"os"}

    def test_visitor_multiple_imports_single_line(self):
        """Test visitor with multiple imports on one line."""
        tree = ast.parse("import os, sys, json")
        visitor = code_search.ImportVisitor()
        visitor.visit(tree)
        assert visitor.imports == {"os", "sys", "json"}

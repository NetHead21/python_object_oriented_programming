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

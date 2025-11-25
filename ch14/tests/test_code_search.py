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

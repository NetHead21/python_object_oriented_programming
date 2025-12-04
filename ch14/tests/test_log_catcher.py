import asyncio
import json
from pathlib import Path
from pytest import fixture, mark, raises
import pickle
import struct
import sys
from unittest.mock import AsyncMock, Mock, call, patch, MagicMock

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import log_catcher


@fixture
def mock_target(monkeypatch):
    open_file = Mock()
    log_catcher.TARGET = open_file
    return open_file


def test_log_writer(mock_target, capsys):
    payload = pickle.dumps("message")
    asyncio.run(log_catcher.log_writer(payload))
    assert mock_target.write.mock_calls == [call('"message"'), call("\n")]


@fixture
def mock_log_writer(monkeypatch):
    log_writer = AsyncMock()
    monkeypatch.setattr(log_catcher, "log_writer", log_writer)
    return log_writer

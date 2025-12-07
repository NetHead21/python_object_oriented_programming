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


@fixture
def mock_stream():
    mock_socket = Mock(getpeername=Mock(return_value=["127.0.0.1", 12342]))
    payload = pickle.dumps("message")
    size = struct.pack(">L", len(payload))
    stream = Mock(
        read=AsyncMock(side_effect=[size, payload, None]),
        get_extra_info=Mock(return_value=mock_socket),
    )
    return payload, stream


def test_log_catcher(mock_log_writer, mock_stream):
    payload, stream = mock_stream
    asyncio.run(log_catcher.log_catcher(stream, stream))
    # Depends on len(payload)
    assert stream.read.mock_calls == [call(4), call(22), call(4)]
    mock_log_writer.assert_awaited_with(payload)


# ============================================================================
# ADDITIONAL COMPREHENSIVE TESTS
# ============================================================================


class TestSerialize:
    """Test suite for serialize function."""

    def test_serialize_simple_dict(self, mock_target):
        """Test serializing a simple dictionary."""
        data = {"level": "INFO", "message": "Test message"}
        payload = pickle.dumps(data)

        result = log_catcher.serialize(payload)

        assert result == json.dumps(data)
        assert mock_target.write.call_count == 2
        mock_target.write.assert_any_call(json.dumps(data))
        mock_target.write.assert_any_call("\n")

    def test_serialize_list(self, mock_target):
        """Test serializing a list."""
        data = [1, 2, 3, "test", {"key": "value"}]
        payload = pickle.dumps(data)

        result = log_catcher.serialize(payload)

        assert result == json.dumps(data)
        mock_target.write.assert_called()

    def test_serialize_string(self, mock_target):
        """Test serializing a simple string."""
        data = "simple string message"
        payload = pickle.dumps(data)

        result = log_catcher.serialize(payload)

        assert result == json.dumps(data)
        assert '"simple string message"' in result

    def test_serialize_number(self, mock_target):
        """Test serializing numeric values."""
        for data in [42, 3.14, -100, 0]:
            payload = pickle.dumps(data)
            result = log_catcher.serialize(payload)
            assert result == json.dumps(data)

    def test_serialize_boolean(self, mock_target):
        """Test serializing boolean values."""
        for data in [True, False]:
            payload = pickle.dumps(data)
            result = log_catcher.serialize(payload)
            assert result == json.dumps(data)

    def test_serialize_none(self, mock_target):
        """Test serializing None value."""
        payload = pickle.dumps(None)
        result = log_catcher.serialize(payload)
        assert result == "null"

    def test_serialize_nested_structure(self, mock_target):
        """Test serializing complex nested structure."""
        data = {
            "level": "ERROR",
            "timestamp": "2025-12-05T10:30:00",
            "details": {
                "error_code": 500,
                "message": "Internal error",
                "stack": ["frame1", "frame2", "frame3"],
            },
            "tags": ["critical", "database"],
        }

        payload = pickle.dumps(data)

        result = log_catcher.serialize(payload)

        assert json.loads(result) == data

    def test_serialize_empty_dict(self, mock_target):
        """Test serializing empty dictionary."""
        payload = pickle.dumps({})
        result = log_catcher.serialize(payload)
        assert result == "{}"

    def test_serialize_empty_list(self, mock_target):
        """Test serializing empty list."""
        payload = pickle.dumps([])
        result = log_catcher.serialize(payload)
        assert result == "[]"


class TestLogWriter:
    """Test suite for log_writer function."""

    def test_log_writer_increments_counter(self, mock_target):
        """Test that log_writer increments LINE_COUNT."""
        initial_count = log_catcher.LINE_COUNT
        payload = pickle.dumps({"msg": "test"})

        asyncio.run(log_catcher.log_writer(payload))

        assert log_catcher.LINE_COUNT == initial_count + 1

    def test_log_writer_multiple_calls(self, mock_target):
        """Test LINE_COUNT with multiple calls."""
        log_catcher.LINE_COUNT = 0
        payloads = [pickle.dumps(f"message {i}") for i in range(5)]

        async def write_all():
            for payload in payloads:
                await log_catcher.log_writer(payload)

        asyncio.run(write_all())
        assert log_catcher.LINE_COUNT == 5

    def test_log_writer_concurrent_calls(self, mock_target):
        """Test concurrent log_writer calls."""
        log_catcher.LINE_COUNT = 0
        payloads = [pickle.dumps(f"message {i}") for i in range(10)]

        async def write_concurrent():
            tasks = [log_catcher.log_writer(p) for p in payloads]
            await asyncio.gather(*tasks)

        asyncio.run(write_concurrent())
        assert log_catcher.LINE_COUNT == 10

    def test_log_writer_with_large_payload(self, mock_target):
        """Test log_writer with large data payload."""
        large_data = {"data": "x" * 10000, "items": list(range(1000))}
        payload = pickle.dumps(large_data)

        asyncio.run(log_catcher.log_writer(payload))

        assert log_catcher.LINE_COUNT > 0
        assert mock_target.write.called


class TestLogCatcher:
    """Test suite for log_catcher function."""

    def test_log_catcher_multiple_messages(self, mock_log_writer):
        """Test log_catcher with multiple messages."""

        mock_socket = Mock(getpeername=Mock(return_value=("127.0.0.1", 12342)))

        messages = [f"message {i}" for i in range(3)]
        payloads = [pickle.dumps(msg) for msg in messages]
        sizes = [struct.pack(">L", len(p)) for p in payloads]

        # Create read side effects: size1, payload1, size2, payload2, size3, payload3, None
        read_effects = []
        for size, payload in zip(sizes, payloads):
            read_effects.extend([size, payload])
        read_effects.append(None)  # End of stream

        stream = Mock(
            read=AsyncMock(side_effect=read_effects),
            get_extra_info=Mock(return_value=mock_socket),
        )

        asyncio.run(log_catcher.log_catcher(stream, stream))

        # Should have read: size, payload for each message, plus final None
        assert stream.read.call_count == 7  # 3 * (size + payload) + 1 (end)
        assert mock_log_writer.await_count == 3

    def test_log_catcher_empty_stream(self, mock_log_writer, capsys):
        """Test log_catcher with immediate disconnect (no messages)."""
        mock_socket = Mock(getpeername=Mock(return_value=("127.0.0.1", 12342)))

        stream = Mock(
            read=AsyncMock(side_effect=[None]),  # Immediate disconnect
            get_extra_info=Mock(return_value=mock_socket),
        )

        asyncio.run(log_catcher.log_catcher(stream, stream))

        out, _ = capsys.readouterr()
        assert "0 lines" in out
        mock_log_writer.assert_not_awaited()

    def test_log_catcher_single_large_message(self, mock_log_writer):
        """Test log_catcher with single large message."""
        mock_socket = Mock(getpeername=Mock(return_value=("127.0.0.1", 12342)))

        large_data = {"data": "x" * 50000}
        payload = pickle.dumps(large_data)
        size = struct.pack(">L", len(payload))

        stream = Mock(
            read=AsyncMock(side_effect=[size, payload, None]),
            get_extra_info=Mock(return_value=mock_socket),
        )

        asyncio.run(log_catcher.log_catcher(stream, stream))

        mock_log_writer.assert_awaited_once()

    def test_log_catcher_different_payload_sizes(self, mock_log_writer):
        """Test log_catcher with varying payload sizes."""
        mock_socket = Mock(getpeername=Mock(return_value=("127.0.0.1", 12342)))

        # Create payloads of different sizes
        payloads = [
            pickle.dumps("small"),
            pickle.dumps({"medium": "data" * 100}),
            pickle.dumps({"large": list(range(1000))}),
        ]

        read_effects = []
        for payload in payloads:
            size = struct.pack(">L", len(payload))
            read_effects.extend([size, payload])
        read_effects.append(None)

        stream = Mock(
            read=AsyncMock(side_effect=read_effects),
            get_extra_info=Mock(return_value=mock_socket),
        )

        asyncio.run(log_catcher.log_catcher(stream, stream))

        assert mock_log_writer.await_count == 3

    def test_log_catcher_prints_client_info(self, mock_log_writer, capsys):
        """Test that log_catcher prints client information."""
        mock_socket = Mock(getpeername=Mock(return_value=("192.168.1.100", 54321)))

        payload = pickle.dumps("test")
        size = struct.pack(">L", len(payload))

        stream = Mock(
            read=AsyncMock(side_effect=[size, payload, None]),
            get_extra_info=Mock(return_value=mock_socket),
        )

        asyncio.run(log_catcher.log_catcher(stream, stream))

        out, _ = capsys.readouterr()
        assert "192.168.1.100" in out
        assert "54321" in out
        assert "1 lines" in out


class TestProtocolConstants:
    """Test suite for protocol constants."""

    def test_size_format_is_big_endian(self):
        """Test that SIZE_FORMAT uses big-endian byte order."""
        assert log_catcher.SIZE_FORMAT == ">L"

    def test_size_bytes_is_four(self):
        """Test that size header is 4 bytes (unsigned long)."""
        assert log_catcher.SIZE_BYTES == 4

    def test_struct_pack_unpack_consistency(self):
        """Test that pack/unpack operations are consistent."""
        test_sizes = [0, 1, 100, 65535, 1000000]

        for size in test_sizes:
            packed = struct.pack(log_catcher.SIZE_FORMAT, size)
            unpacked = struct.unpack(log_catcher.SIZE_FORMAT, packed)
            assert unpacked[0] == size
            assert len(packed) == log_catcher.SIZE_BYTES


class TestEdgeCases:
    """Edge case tests for the log catcher."""

    def test_serialize_with_unicode_characters(self, mock_target):
        """Test serializing data with Unicode characters."""
        data = {"message": "Hello 世界 🌍", "emoji": "😀🎉✨", "special": "àéîöü"}
        payload = pickle.dumps(data)

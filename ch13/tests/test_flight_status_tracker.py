import datetime
from unittest.mock import Mock, patch, call
import pytest
import sys
from pathlib import Path


# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))
from src import flight_status_redis


@pytest.fixture
def mock_redis() -> Mock:
    mock_redis_instance = Mock(set=Mock(return_value=True))
    return mock_redis_instance


@pytest.fixture
def tracker(
    monkeypatch: pytest.MonkeyPatch, mock_redis: Mock
) -> flight_status_redis.FlightStatusTracker:
    """Depending on the test scenario, this may require a running REDIS server."""
    fst = flight_status_redis.FlightStatusTracker()
    monkeypatch.setattr(fst, "redis", mock_redis)
    return fst


def test_monkeypatch_class(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    with pytest.raises(ValueError) as ex:
        tracker.change_status("AC101", "lost")
    assert ex.value.args[0] == "'lost' is not a valid Status"
    assert mock_redis.set.call_count == 0


def test_patch_class(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    fake_now = datetime.datetime(2020, 10, 26, 23, 24, 25)
    utc = datetime.timezone.utc
    with patch("src.flight_status_redis.datetime") as mock_datetime:
        mock_datetime.datetime = Mock(now=Mock(return_value=fake_now))
        mock_datetime.timezone = Mock(utc=utc)
        tracker.change_status("AC101", flight_status_redis.Status.ON_TIME)
    mock_datetime.datetime.now.assert_called_once_with(tz=utc)
    expected = "2020-10-26T23:24:25 | ON TIME"
    mock_redis.set.assert_called_once_with("flightno:AC101", expected)

    assert mock_datetime.datetime.now.mock_calls == [call(tz=utc)]
    assert mock_redis.set.mock_calls == [call("flightno:AC101", expected)]


def test_patch_class_2(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    mock_datetime_now = Mock(return_value=datetime.datetime(2020, 10, 26, 23, 24, 25))
    with patch("src.flight_status_redis.datetime.datetime", now=mock_datetime_now):
        tracker.change_status("AC101", flight_status_redis.Status.ON_TIME)
    mock_datetime_now.assert_called_once_with(tz=datetime.timezone.utc)
    expected = "2020-10-26T23:24:25 | ON TIME"
    mock_redis.set.assert_called_once_with("flightno:AC101", expected)

    assert mock_datetime_now.mock_calls == [call(tz=datetime.timezone.utc)]
    assert mock_redis.set.mock_calls == [call("flightno:AC101", expected)]


# === Edge Case Tests ===


def test_change_status_all_status_types(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test that all Status enum values can be set."""
    fake_now = datetime.datetime(2020, 10, 26, 23, 24, 25)

    with patch("src.flight_status_redis.datetime.datetime") as mock_dt:
        mock_dt.now = Mock(return_value=fake_now)

        # Test CANCELLED
        tracker.change_status("FL001", flight_status_redis.Status.CANCELLED)
        # Test DELAYED
        tracker.change_status("FL002", flight_status_redis.Status.DELAYED)
        # Test ON_TIME
        tracker.change_status("FL003", flight_status_redis.Status.ON_TIME)

    assert mock_redis.set.call_count == 3


def test_change_status_invalid_type_none(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test that None is rejected as invalid status."""
    with pytest.raises(ValueError) as ex:
        tracker.change_status("FL123", None)
    assert "is not a valid Status" in str(ex.value)
    assert mock_redis.set.call_count == 0


def test_change_status_invalid_type_integer(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test that integer is rejected as invalid status."""
    with pytest.raises(ValueError) as ex:
        tracker.change_status("FL123", 1)
    assert "is not a valid Status" in str(ex.value)
    assert mock_redis.set.call_count == 0


def test_change_status_invalid_type_dict(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test that dict is rejected as invalid status."""
    with pytest.raises(ValueError) as ex:
        tracker.change_status("FL123", {"status": "ON_TIME"})
    assert "is not a valid Status" in str(ex.value)
    assert mock_redis.set.call_count == 0


def test_change_status_empty_flight_number(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test that empty flight number is allowed (edge case)."""
    fake_now = datetime.datetime(2020, 10, 26, 23, 24, 25)

    with patch("src.flight_status_redis.datetime.datetime") as mock_dt:
        mock_dt.now = Mock(return_value=fake_now)
        tracker.change_status("", flight_status_redis.Status.ON_TIME)

    expected = "2020-10-26T23:24:25 | ON TIME"
    mock_redis.set.assert_called_once_with("flightno:", expected)


def test_change_status_special_characters_in_flight_number(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test flight numbers with special characters."""
    fake_now = datetime.datetime(2020, 10, 26, 23, 24, 25)

    with patch("src.flight_status_redis.datetime.datetime") as mock_dt:
        mock_dt.now = Mock(return_value=fake_now)
        tracker.change_status("FL-123/A", flight_status_redis.Status.DELAYED)

    expected = "2020-10-26T23:24:25 | DELAYED"
    mock_redis.set.assert_called_once_with("flightno:FL-123/A", expected)


def test_change_status_very_long_flight_number(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test very long flight number (stress test)."""
    fake_now = datetime.datetime(2020, 10, 26, 23, 24, 25)
    long_flight = "A" * 1000

    with patch("src.flight_status_redis.datetime.datetime") as mock_dt:
        mock_dt.now = Mock(return_value=fake_now)
        tracker.change_status(long_flight, flight_status_redis.Status.ON_TIME)

    expected = "2020-10-26T23:24:25 | ON TIME"
    mock_redis.set.assert_called_once_with(f"flightno:{long_flight}", expected)


def test_change_status_updates_existing_flight(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test that changing status multiple times for same flight works."""
    fake_now = datetime.datetime(2020, 10, 26, 23, 24, 25)

    with patch("src.flight_status_redis.datetime.datetime") as mock_dt:
        mock_dt.now = Mock(return_value=fake_now)
        tracker.change_status("FL100", flight_status_redis.Status.ON_TIME)
        tracker.change_status("FL100", flight_status_redis.Status.DELAYED)
        tracker.change_status("FL100", flight_status_redis.Status.CANCELLED)

    assert mock_redis.set.call_count == 3
    # Last call should be CANCELLED
    last_call = mock_redis.set.call_args_list[-1]
    assert last_call[0][0] == "flightno:FL100"
    assert "CANCELLED" in last_call[0][1]


def test_get_status_flight_not_found(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test getting status for non-existent flight returns None, None."""
    mock_redis.get = Mock(return_value=None)

    timestamp, status = tracker.get_status("NONEXISTENT")

    assert timestamp is None
    assert status is None
    mock_redis.get.assert_called_once_with("flightno:NONEXISTENT")


def test_get_status_valid_flight(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test getting status for existing flight."""
    mock_value = "2020-10-26T23:24:25 | ON TIME"
    mock_redis.get = Mock(return_value=mock_value)

    timestamp, status = tracker.get_status("FL200")

    assert timestamp == datetime.datetime(2020, 10, 26, 23, 24, 25)
    assert status == flight_status_redis.Status.ON_TIME
    mock_redis.get.assert_called_once_with("flightno:FL200")


def test_get_status_cancelled_flight(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test getting CANCELLED status."""
    mock_value = "2020-11-15T10:30:00 | CANCELLED"
    mock_redis.get = Mock(return_value=mock_value)

    timestamp, status = tracker.get_status("FL300")

    assert timestamp == datetime.datetime(2020, 11, 15, 10, 30, 0)
    assert status == flight_status_redis.Status.CANCELLED


def test_get_status_delayed_flight(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test getting DELAYED status."""
    mock_value = "2020-12-01T14:45:30 | DELAYED"
    mock_redis.get = Mock(return_value=mock_value)

    timestamp, status = tracker.get_status("FL400")

    assert timestamp == datetime.datetime(2020, 12, 1, 14, 45, 30)
    assert status == flight_status_redis.Status.DELAYED


def test_get_status_with_microseconds(
    tracker: flight_status_redis.FlightStatusTracker, mock_redis: Mock
) -> None:
    """Test parsing timestamp with microseconds."""
    mock_value = "2020-10-26T23:24:25.123456 | ON TIME"
    mock_redis.get = Mock(return_value=mock_value)

    timestamp, status = tracker.get_status("FL500")

    assert timestamp == datetime.datetime(2020, 10, 26, 23, 24, 25, 123456)
    assert status == flight_status_redis.Status.ON_TIME

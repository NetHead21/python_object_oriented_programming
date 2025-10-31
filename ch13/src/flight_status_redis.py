"""Flight status tracking system using Redis for data persistence.

This module implements a flight status tracking system that uses Redis as a backend
to store and retrieve flight status information with timestamps. The system tracks
flight status changes (CANCELLED, DELAYED, ON_TIME) and provides historical lookup.

Redis is used as a key-value store where:
- Key: "flightno:{flight_number}"
- Value: "{ISO_timestamp} | {status_value}"

Dependencies:
    - redis-py: Python client for Redis
    - Redis server must be running on localhost:6379 (default configuration)

Example:
    Basic usage:

        >>> from flight_status_redis import FlightStatusTracker, Status
        >>> tracker = FlightStatusTracker()
        >>> tracker.change_status("AA123", Status.ON_TIME)
        >>> timestamp, status = tracker.get_status("AA123")
        >>> print(f"Flight AA123 is {status} as of {timestamp}")

Attributes:
    Status (Enum): Enumeration of valid flight status values.
    FlightStatusTracker (class): Main tracker using hardcoded Redis connection.
    FlightStatusTracker_Alt (class): Alternative tracker supporting dependency injection.
"""

import datetime
from enum import Enum
import redis
from typing import Optional


class Status(str, Enum):
    """Enumeration of valid flight status values.

    This enum defines the three possible states for a flight. It inherits from
    both str and Enum, making instances directly comparable to strings and
    serializable without additional conversion.

    Attributes:
        CANCELLED: Flight has been cancelled
        DELAYED: Flight is delayed from scheduled time
        ON_TIME: Flight is on schedule

    Example:
        >>> status = Status.ON_TIME
        >>> print(status.value)
        'ON TIME'
        >>> status == "ON TIME"
        True
    """

    CANCELLED = "CANCELLED"
    DELAYED = "DELAYED"
    ON_TIME = "ON TIME"


class FlightStatusTracker:
    """Track flight status changes using Redis for persistence.

    This class provides methods to update and retrieve flight status information
    stored in a Redis database. Each status change is timestamped with the current
    UTC time.

    The Redis connection is hardcoded to localhost:6379 database 0. For more
    flexible configuration, consider using FlightStatusTracker_Alt instead.

    Attributes:
        redis (redis.Redis): Redis client connection instance.

    Example:
        >>> tracker = FlightStatusTracker()
        >>> tracker.change_status("DL456", Status.DELAYED)
        >>> timestamp, status = tracker.get_status("DL456")
        >>> print(f"Status: {status}, Updated: {timestamp}")
    """

    def __init__(self) -> None:
        """Initialize the flight status tracker with Redis connection.

        Creates a Redis connection to localhost:6379, database 0.

        Raises:
            redis.ConnectionError: If unable to connect to Redis server.
        """
        self.redis = redis.Redis(host="127.0.0.1", port=6379, db=0)

    def change_status(self, flight: str, status: Status) -> None:
        """Update the status of a flight in Redis.

        Records a new status for the specified flight with the current UTC timestamp.
        The data is stored in Redis with key format "flightno:{flight}" and value
        format "{ISO_timestamp} | {status_value}".

        Args:
            flight (str): Flight number/identifier (e.g., "AA123", "DL456").
            status (Status): New status from the Status enum.

        Returns:
            None

        Raises:
            ValueError: If status is not a valid Status enum instance.
            redis.ConnectionError: If Redis connection fails.

        Example:
            >>> tracker = FlightStatusTracker()
            >>> tracker.change_status("UA789", Status.ON_TIME)
            >>> tracker.change_status("SW101", Status.DELAYED)

        Note:
            This overwrites any previous status for the flight. No history is kept.
        """

        if not isinstance(status, Status):
            raise ValueError(f"{status!r} is not a valid Status")
        key = f"flightno:{flight}"
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        value = f"{now.isoformat()} | {status.value}"
        self.redis.set(key, value)

    def get_status(
        self, flight: str
    ) -> tuple[Optional[datetime.datetime], Optional[Status]]:
        """Retrieve the current status of a flight from Redis.

        Looks up the flight status in Redis and parses the stored timestamp
        and status value. If the flight is not found, returns (None, None).

        Args:
            flight (str): Flight number/identifier to look up.

        Returns:
            tuple[Optional[datetime.datetime], Optional[Status]]: A tuple containing:
                - timestamp: When the status was last updated (timezone-aware), or None
                - status: Current Status enum value, or None

        Raises:
            redis.ConnectionError: If Redis connection fails.
            ValueError: If stored status value is not a valid Status enum value.

        Example:
            >>> tracker = FlightStatusTracker()
            >>> tracker.change_status("BA200", Status.ON_TIME)
            >>> timestamp, status = tracker.get_status("BA200")
            >>> if status:
            ...     print(f"Flight BA200: {status} as of {timestamp}")

            # Non-existent flight
            >>> timestamp, status = tracker.get_status("FAKE123")
            >>> print(timestamp, status)
            None None

        Note:
            The returned datetime is timezone-aware (UTC). The status string is
            parsed back into a Status enum instance.
        """
        key = f"flightno:{flight}"
        value = self.redis.get(key)
        if value:
            text_timestamp, text_status = value.split("|")
            timestamp = datetime.datetime.fromisoformat(text_timestamp.strip())
            status = Status(text_status.strip())
            return timestamp, status
        return None, None


class FlightStatusTracker_Alt:
    """Alternative flight status tracker with dependency injection support.

    This is an improved version of FlightStatusTracker that allows injecting a
    custom Redis connection, making it more testable and flexible. If no Redis
    instance is provided, it creates a default connection to localhost:6379.

    This class demonstrates the Dependency Injection pattern, allowing for:
    - Easy unit testing with mock Redis instances
    - Configuration of Redis connection parameters
    - Use of Redis clusters or alternative configurations

    Attributes:
        redis (redis.Connection): Redis client connection instance.

    Example:
        # Using default connection
        >>> tracker = FlightStatusTracker_Alt()

        # Using custom connection
        >>> import redis
        >>> custom_redis = redis.Redis(host="redis.example.com", port=6380, db=1)
        >>> tracker = FlightStatusTracker_Alt(redis_instance=custom_redis)

        # Using mock for testing
        >>> from unittest.mock import Mock
        >>> mock_redis = Mock()
        >>> tracker = FlightStatusTracker_Alt(redis_instance=mock_redis)
    """

    def __init__(self, redis_instance: Optional[redis.Connection] = None) -> None:
        """Initialize tracker with optional Redis connection injection.

        Args:
            redis_instance (Optional[redis.Connection]): Custom Redis connection
                to use. If None, creates a default connection to localhost:6379, db=0.

        Example:
            >>> tracker = FlightStatusTracker_Alt()  # Uses default
            >>>
            >>> custom = redis.Redis(host="10.0.0.1", port=6379, db=2)
            >>> tracker = FlightStatusTracker_Alt(redis_instance=custom)
        """
        self.redis = (
            redis_instance
            if redis_instance
            else redis.Redis(host="127.0.0.1", port=6379, db=0)
        )


def demo() -> None:
    """Demonstrate basic usage of the FlightStatusTracker.

    Creates a tracker instance, sets a flight status to ON_TIME, retrieves it,
    and prints the timestamp and status to console.

    This function is meant for testing and demonstration purposes.

    Returns:
        None

    Side Effects:
        - Connects to Redis at localhost:6379
        - Sets flight "42" status to ON_TIME
        - Prints timestamp and status to stdout

    Example:
        $ python flight_status_redis.py
        2025-10-19 10:30:45.123456+00:00 Status.ON_TIME

    Note:
        Will fail if Redis server is not running on localhost:6379.
    """
    fst = FlightStatusTracker()
    fst.change_status("42", Status.ON_TIME)
    as_of, status = fst.get_status("42")
    print(as_of, status)


if __name__ == "__main__":
    demo()

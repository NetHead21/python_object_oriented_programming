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

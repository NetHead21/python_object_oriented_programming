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

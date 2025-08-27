"""
GPS Message Parsing and Flyweight Pattern Demo

This module provides a comprehensive implementation for parsing NMEA GPS messages (GPGGA, GPGLL, GPRMC)
using object-oriented design principles and the flyweight pattern. It demonstrates robust parsing,
field extraction, and conversion to geographic coordinates with extensive error handling and validation.

The implementation showcases several design patterns:
- Flyweight Pattern: Message factory creates reusable message objects
- Template Method Pattern: Abstract Message class defines parsing structure
- Strategy Pattern: Different concrete message classes handle specific formats
- Adapter Pattern: Buffer class adapts bytes for sequence operations

Key Features:
- Type-safe parsing with comprehensive error handling
- Memory-efficient flyweight message objects
- Flexible buffer abstraction for byte-wise access
- Robust field extraction with bounds checking
- Geographic coordinate conversion and formatting
- Support for multiple NMEA message formats
- Batch processing of multiple GPS messages

Supported NMEA Message Types:
- GPGGA: GPS Fix Data (time, position, fix quality indicators)
- GPGLL: Geographic Position (latitude/longitude and time)
- GPRMC: Recommended Minimum (position, velocity, time, date)

Example Usage:
    >>> buffer = Buffer(b"$GPGLL,3751.65,S,14507.36,E*77")
    >>> message = message_factory(buffer[1:6])
    >>> if message:
    ...     fix = message.from_buffer(buffer, 0).get_fix()
    ...     print(fix)  # (37°51.6500'S, 145°07.3600'E)
"""
    """
GPS Message Parsing and Flyweight Pattern Demo

This module provides a comprehensive implementation for parsing NMEA GPS messages (GPGGA, GPGLL, GPRMC)
using object-oriented design principles and the flyweight pattern. It demonstrates robust parsing,
field extraction, and conversion to geographic coordinates with extensive error handling and validation.

The implementation showcases several design patterns:
- Flyweight Pattern: Message factory creates reusable message objects
- Template Method Pattern: Abstract Message class defines parsing structure
- Strategy Pattern: Different concrete message classes handle specific formats
- Adapter Pattern: Buffer class adapts bytes for sequence operations

Key Features:
- Type-safe parsing with comprehensive error handling
- Memory-efficient flyweight message objects
- Flexible buffer abstraction for byte-wise access
- Robust field extraction with bounds checking
- Geographic coordinate conversion and formatting
- Support for multiple NMEA message formats
- Batch processing of multiple GPS messages

Supported NMEA Message Types:
- GPGGA: GPS Fix Data (time, position, fix quality indicators)
- GPGLL: Geographic Position (latitude/longitude and time)
- GPRMC: Recommended Minimum (position, velocity, time, date)

Example Usage:
    >>> buffer = Buffer(b"$GPGLL,3751.65,S,14507.36,E*77")
    >>> message = message_factory(buffer[1:6])
    >>> if message:
    ...     fix = message.from_buffer(buffer, 0).get_fix()
    ...     print(fix)  # (37°51.6500'S, 145°07.3600'E)
"""


import abc
import weakref
from dataclasses import dataclass
from math import radians, floor
from typing import Optional, cast, overload, Sequence, Iterator


class GPSParsingError(Exception):
    """Raised when GPS message parsing fails due to invalid format."""

    pass

class GPSValidationError(Exception):
    """Raised when GPS data validation fails."""

    pass

class GPSError(Exception):
    """
    Base class for GPS-related errors.

    This serves as the parent class for all GPS-specific exceptions,
    allowing for comprehensive error handling in GPS processing pipelines.
    """

    pass


@dataclass(frozen=True)
class Point:
    """
    Represents a geographic point with latitude and longitude coordinates.

    This immutable dataclass provides conversion from NMEA GPS message byte fields
    to decimal degrees, along with string formatting and coordinate validation.
    Supports both decimal degrees and degrees/minutes formats.

    Coordinate Ranges:
    - Latitude: -90.0 to +90.0 degrees (S to N)
    - Longitude: -180.0 to +180.0 degrees (W to E)

    Attributes:
        latitude (float): Latitude in decimal degrees (-90 to +90)
        longitude (float): Longitude in decimal degrees (-180 to +180)

    Example:
        >>> point = Point(37.8608, -122.2083)  # San Francisco
        >>> str(point)  # "(37°51.6500'N, 122°12.5000'W)"
        >>> point.lat  # Latitude in radians
    """

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        """Validate coordinates after initialization."""
        if not isinstance(self.latitude, (int, float)):
            raise GPSValidationError(
                f"Latitude must be numeric, got {type(self.latitude)}"
            )
        if not isinstance(self.longitude, (int, float)):
            raise GPSValidationError(
                f"Longitude must be numeric, got {type(self.longitude)}"
            )

        if not (-90.0 <= self.latitude <= 90.0):
            raise GPSValidationError(
                f"Latitude {self.latitude} out of range (-90 to +90)"
            )
        if not (-180.0 <= self.longitude <= 180.0):
            raise GPSValidationError(
                f"Longitude {self.longitude} out of range (-180 to +180)"
            )
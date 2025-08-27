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

    @classmethod
    def from_bytes(
        cls, latitude: bytes, N_S: bytes, longitude: bytes, E_W: bytes
    ) -> "Point":
        """
        Convert NMEA latitude/longitude byte fields to a Point.

        NMEA format uses DDMM.MMMM for latitude and DDDMM.MMMM for longitude,
        where DD/DDD are degrees and MM.MMMM are decimal minutes.

        Args:
            latitude (bytes): Latitude in DDMM.MMMM format (e.g., b"3751.65")
            N_S (bytes): North/South indicator (b"N" or b"S")
            longitude (bytes): Longitude in DDDMM.MMMM format (e.g., b"12158.34")
            E_W (bytes): East/West indicator (b"E" or b"W")

        Returns:
            Point: Geographic point with decimal degree coordinates

        Raises:
            GPSParsingError: If byte fields cannot be parsed
            GPSValidationError: If coordinates are out of valid range

        Example:
            >>> Point.from_bytes(b"3751.65", b"S", b"14507.36", b"E")
            Point(latitude=-37.8608333, longitude=145.1226667)
        """

        try:
            # Parse latitude (DDMM.MMMM format)
            if len(latitude) < 4:
                raise GPSParsingError(f"Latitude field too short: {latitude}")
            lat_deg = float(latitude[:2])
            lat_min = float(latitude[2:])
            lat_decimal = lat_deg + lat_min / 60.0
            lat_sign = 1 if N_S.upper() == b"N" else -1

            # Parse longitude (DDDMM.MMMM format)
            if len(longitude) < 5:
                raise GPSParsingError(f"Longitude field too short: {longitude}")
            lon_deg = float(longitude[:3])
            lon_min = float(longitude[3:])
            lon_decimal = lon_deg + lon_min / 60.0
            lon_sign = 1 if E_W.upper() == b"E" else -1

            return cls(lat_decimal * lat_sign, lon_decimal * lon_sign)
        
        except ValueError as e:
            raise GPSParsingError(f"Failed to parse coordinates: {e}")
        except Exception as e:
            raise GPSParsingError(f"Unexpected error parsing coordinates: {e}")

    def __str__(self) -> str:
        """
        Format coordinates as human-readable degrees/minutes string.

        Returns:
            str: Formatted string like "(37°51.6500'N, 122°12.5000'W)"
        """

        lat = abs(self.latitude)
        lat_deg = floor(lat)
        lat_min = (lat - lat_deg) * 60
        lat_dir = "N" if self.latitude >= 0 else "S"

        lon = abs(self.longitude)
        lon_deg = floor(lon)
        lon_min = (lon - lon_deg) * 60
        lon_dir = "E" if self.longitude >= 0 else "W"

        return (
            f"({lat_deg:02.0f}°{lat_min:07.4f}'{lat_dir}, "
            f"{lon_deg:03.0f}°{lon_min:07.4f}'{lon_dir})"
        )


    @property
    def lat(self) -> float:
        """Latitude in radians."""
        return radians(self.latitude)


    @property
    def lon(self) -> float:
        """Longitude in radians."""
        return radians(self.longitude)
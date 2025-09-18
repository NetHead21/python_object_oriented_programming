"""GPS Message Parser with Flyweight and Slots Optimization.

This module provides a memory-efficient GPS message parsing system that demonstrates
the Flyweight pattern combined with Python's __slots__ for optimal memory usage.

The module handles three types of NMEA GPS messages:
- GPGGA: Global Positioning System Fix Data
- GPGLL: Geographic Position - Latitude/Longitude
- GPRMC: Recommended Minimum Navigation Information

Key Features:
- Memory-efficient parsing using __slots__
- Flyweight pattern for message object reuse
- Weak references to prevent memory leaks
- Support for multiple GPS message formats
- Automatic coordinate parsing and formatting

Classes:
    Point: Represents geographic coordinates with lat/lon
    Buffer: Memory-efficient byte sequence wrapper
    Message: Abstract base class for GPS messages
    GPGGA, GPGLL, GPRMC: Concrete GPS message implementations
    Client: GPS message stream processor

Example:
    # Parse a GPS message buffer
    buffer = Buffer(b"$GPGGA,170834,4124.8963,N,08151.6838,W,1,05,1.5,280.2,M,-34.0,M,,*75")
    client = Client(buffer)
    client.scan()  # Prints parsed coordinates
"""

import abc
import weakref
from math import radians, floor
from typing import Optional, overload, Sequence, Iterator, cast


class Point:
    """Represents a geographic point with latitude and longitude coordinates.

    This class uses __slots__ for memory efficiency and provides methods for
    parsing GPS coordinates from NMEA message format and formatting them
    for display.

    Attributes:
        latitude (float): Latitude in decimal degrees (-90 to +90)
        longitude (float): Longitude in decimal degrees (-180 to +180)

    Example:
        >>> point = Point(49.274167, -123.185833)  # Vancouver, BC
        >>> print(point)
        49°16.4500'N, 123°11.1500'W
    """

    __slots__ = ("latitude", "longitude")

    def __init__(self, latitude: float, longitude: float) -> None:
        """Initialize a Point with latitude and longitude.

        Args:
            latitude (float): Latitude in decimal degrees
            longitude (float): Longitude in decimal degrees
        """
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self) -> str:
        """Return a detailed string representation for debugging.

        Returns:
            str: String in format "Point(latitude=XX.XX, longitude=YY.YY)"
        """
        return f"Point(latitude={self.latitude}, longitude={self.longitude})"

    @classmethod
    def from_bytes(
        cls,
        latitude: bytes,
        N_S: bytes,
        longitude: bytes,
        E_W: bytes,
    ) -> "Point":
        """Create a Point from GPS coordinate byte strings.

        Parses GPS coordinates from NMEA format (DDMM.MMMM for latitude,
        DDDMM.MMMM for longitude) and converts them to decimal degrees.

        Args:
            latitude (bytes): Latitude in DDMM.MMMM format
            N_S (bytes): Latitude direction ('N' or 'S')
            longitude (bytes): Longitude in DDDMM.MMMM format
            E_W (bytes): Longitude direction ('E' or 'W')

        Returns:
            Point: New Point instance with parsed coordinates

        Example:
            >>> point = Point.from_bytes(b"4916.45", b"N", b"12311.12", b"W")
            >>> print(point.latitude, point.longitude)
            49.274167 -123.185333
        """

        # Parse latitude: DDMM.MMMM format
        lat_str = latitude.decode("ascii")
        lat_deg = float(lat_str[:2])  # First 2 digits are degrees
        lat_min = float(lat_str[2:])  # Rest are minutes
        lat_decimal = lat_deg + lat_min / 60
        lat_sign = 1 if N_S.upper() == b"N" else -1

        # Parse longitude: DDDMM.MMMM format
        lon_str = longitude.decode("ascii")
        lon_deg = float(lon_str[:3])  # First 3 digits are degrees
        lon_min = float(lon_str[3:])  # Rest are minutes
        lon_decimal = lon_deg + lon_min / 60
        lon_sign = 1 if E_W.upper() == b"E" else -1

        return cls(lat_decimal * lat_sign, lon_decimal * lon_sign)

    def __str__(self) -> str:
        """Return a human-readable string representation of the coordinates.

        Formats coordinates in degrees, minutes format (DD°MM.MMMM'X).

        Returns:
            str: Formatted coordinates like "49°16.4500'N, 123°11.1200'W"
        """

        lat = abs(self.latitude)
        lat_deg = floor(lat)
        lat_min_sec = 60 * (lat - lat_deg)
        lat_dir = "N" if self.latitude >= 0 else "S"
        lon = abs(self.longitude)
        lon_deg = floor(lon)
        lon_min_sec = 60 * (lon - lon_deg)
        lon_dir = "E" if self.longitude >= 0 else "W"
        return (
            f"{lat_deg:02.0f}°{lat_min_sec:07.4f}'{lat_dir}, "
            f"{lon_deg:03.0f}°{lon_min_sec:07.4f}'{lon_dir}"
        )

    @property
    def lat(self) -> float:
        """Get latitude in radians.

        Returns:
            float: Latitude converted to radians
        """
        return radians(self.latitude)

    @property
    def lon(self) -> float:
        """Get longitude in radians.

        Returns:
            float: Longitude converted to radians
        """
        return radians(self.longitude)


p = Point.from_bytes(b"4916.45", b"N", b"12311.12", b"W")
print(p)


class Buffer(Sequence[int]):
    """Memory-efficient wrapper for byte sequences used in GPS message parsing.

    Implements the Sequence protocol to provide indexing and iteration over
    bytes as integers. This allows for efficient parsing of GPS message data
    without copying the underlying byte data.

    Attributes:
        content (bytes): The underlying byte data

    Example:
        >>> buffer = Buffer(b"$GPGGA,170834")
        >>> buffer[0]  # First byte as int
        36
        >>> chr(buffer[0])  # Convert to character
        '$'
        >>> len(buffer)
        14
    """

    def __init__(self, content: bytes) -> None:
        """Initialize the buffer with byte content.

        Args:
            content (bytes): The byte data to wrap
        """
        self.content = content

    def __len__(self) -> int:
        """Return the length of the buffer.

        Returns:
            int: Number of bytes in the buffer
        """

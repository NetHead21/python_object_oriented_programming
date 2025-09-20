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
        return len(self.content)

    def __iter__(self) -> Iterator[int]:
        """Iterate over buffer contents as integers.

        Returns:
            Iterator[int]: Iterator yielding each byte as an integer
        """
        return iter(self.content)

    @overload
    def __getitem__(self, index: int) -> int:
        """Get a single byte as an integer."""
        ...

    @overload
    def __getitem__(self, index: slice) -> bytes:
        """Get a slice of bytes."""
        ...

    def __getitem__(self, index: int | slice) -> int | bytes:
        """Get item(s) from the buffer by index or slice.

        Args:
            index: Either an integer index or a slice object

        Returns:
            int: Single byte as integer if index is int
            bytes: Byte sequence if index is slice

        Example:
            >>> buffer = Buffer(b"Hello")
            >>> buffer[0]  # Single byte
            72
            >>> buffer[1:3]  # Slice
            b'el'
        """
        return self.content[index]


class GPSError(Exception):
    """Exception raised when GPS message parsing encounters an error.

    This exception is raised when:
    - A GPS message is incomplete or malformed
    - Required message terminator '*' is not found
    - Buffer contains invalid GPS data
    """

    pass


class Message:
    """Abstract base class for GPS message parsing using the Flyweight pattern.

    This class provides common functionality for parsing NMEA GPS messages.
    Uses __slots__ for memory efficiency and weak references to prevent
    memory leaks when multiple messages reference the same buffer.

    The Flyweight pattern is implemented by:
    - Sharing buffer references across multiple message instances
    - Using weak references to allow garbage collection
    - Storing only intrinsic state (parsing positions, not actual data)

    Attributes:
        buffer (weakref.ReferenceType[Buffer]): Weak reference to message buffer
        offset (int): Starting position of message in buffer
        end (Optional[int]): Ending position of message in buffer
        commas (list[int]): Positions of comma separators in message
    """

    __slots__ = ("buffer", "offset", "end", "commas")

    def __init__(self) -> None:
        """Initialize an empty message parser."""
        self.buffer: weakref.ReferenceType[Buffer]
        self.offset = 0
        self.end: Optional[int]
        self.commas: list[int]

    def from_buffer(self, buffer: Buffer, offset: int) -> "Message":
        """Parse a GPS message from the buffer starting at the given offset.

        Sets up the message parsing state by finding comma separators and
        the message terminator. Creates a weak reference to the buffer to
        avoid circular references.

        Args:
            buffer (Buffer): The buffer containing GPS message data
            offset (int): Starting position of the message in the buffer

        Returns:
            Message: Self, for method chaining

        Raises:
            GPSError: If no message terminator '*' is found within 82 bytes
        """

        self.buffer = weakref.ref(buffer)
        self.offset = offset
        self.commas = [offset]
        self.end = None
        for index in range(offset, offset + 82):
            if buffer[index] == ord(b","):
                self.commas.append(index)
            elif buffer[index] == ord(b"*"):
                self.commas.append(index)
                self.end = index + 3
                break
        if self.end is None:
            raise GPSError("No end found")
        return self

    def __getitem__(self, field: int) -> bytes:
        """Extract a field from the parsed message by field number.

        Fields are separated by commas in NMEA messages. This method
        returns the bytes between comma positions.

        Args:
            field (int): Field number to extract (0-based)

        Returns:
            bytes: The field content as bytes

        Raises:
            RuntimeError: If the buffer reference has been garbage collected
        """
        if not hasattr(self, "buffer") or (buffer := self.buffer()) is None:
            raise RuntimeError("Broken reference")
        start, end = self.commas[field] + 1, self.commas[field + 1]
        return buffer[start:end]

    def get_fix(self) -> Point:
        """Extract and parse the GPS position fix from the message.

        Calls the abstract methods to get latitude, longitude and direction
        indicators, then creates a Point object with the parsed coordinates.

        Returns:
            Point: Geographic coordinates parsed from the message
        """
        return Point.from_bytes(
            self.latitude(), self.lat_n_s(), self.longitude(), self.lon_e_w()
        )

    @abc.abstractmethod
    def latitude(self) -> bytes:
        """Extract latitude field from the message.

        Returns:
            bytes: Latitude in DDMM.MMMM format
        """
        ...

    @abc.abstractmethod
    def lat_n_s(self) -> bytes:
        """Extract latitude direction indicator from the message.

        Returns:
            bytes: Either b'N' (North) or b'S' (South)
        """
        ...

    @abc.abstractmethod
    def longitude(self) -> bytes:
        """Extract longitude field from the message.

        Returns:
            bytes: Longitude in DDDMM.MMMM format
        """
        ...

    @abc.abstractmethod
    def lon_e_w(self) -> bytes:
        """Extract longitude direction indicator from the message.

        Returns:
            bytes: Either b'E' (East) or b'W' (West)
        """
        ...


class GPGGA(Message):
    """Parser for GPGGA (Global Positioning System Fix Data) messages.

    GPGGA messages provide essential GPS fix information including:
    - Time of fix
    - Latitude and longitude
    - Fix quality indicator
    - Number of satellites
    - Horizontal dilution of precision
    - Altitude above mean sea level

    Message format:
    $GPGGA,hhmmss.ss,ddmm.mmmm,a,dddmm.mmmm,b,q,xx,p.p,a.a,M,g.g,M,s,cccc*hh

    Field positions:
    - Field 2: Latitude (ddmm.mmmm)
    - Field 3: Latitude direction (N/S)
    - Field 4: Longitude (dddmm.mmmm)
    - Field 5: Longitude direction (E/W)
    """

    __slots__ = ()

    def latitude(self) -> bytes:
        """Get latitude field from GPGGA message (field 2)."""
        return self[2]

    def lat_n_s(self) -> bytes:
        """Get latitude direction from GPGGA message (field 3)."""
        return self[3]

    def longitude(self) -> bytes:
        """Get longitude field from GPGGA message (field 4)."""
        return self[4]

    def lon_e_w(self) -> bytes:
        """Get longitude direction from GPGGA message (field 5)."""
        return self[5]


raw = Buffer(b"$GPGGA,170834,4124.8963,N,08151.6838,W,1,05,1.5,280.2,M,-34.0,M,,*75")

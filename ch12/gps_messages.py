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

    def distance_to(self, other: "Point") -> float:
        """
        Calculate great circle distance to another point using haversine formula.

        Args:
            other (Point): Target point

        Returns:
            float: Distance in kilometers
        """

        from math import sin, cos, sqrt, atan2

        # Earth radius in kilometers
        R = 6371.0

        # Convert to radians
        lat1, lon1 = self.lat, self.lon
        lat2, lon2 = other.lat, other.lon

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c


class Buffer(Sequence[int]):
    """
    Buffer abstraction for byte-wise access to GPS message data.

    This class wraps a bytes object and provides sequence-like access with both
    integer access (for individual byte values) and slice access (for byte ranges).
    It's designed to work efficiently with GPS message parsing where you need to
    examine individual bytes and extract field ranges.

    The buffer supports:
    - Integer indexing: Returns byte value as int (0-255)
    - Slice indexing: Returns bytes object for the slice
    - Length operations and iteration
    - Memory-efficient reference to underlying bytes

    Example:
        >>> buf = Buffer(b"$GPGLL,3751.65,S*77")
        >>> buf[0]  # Returns 36 (ASCII for '$')
        >>> buf[1:6]  # Returns b'GPGLL'
        >>> len(buf)  # Returns 19
    """

    def __init__(self, content: bytes) -> None:
        """
        Initialize buffer with bytes content.

        Args:
            content (bytes): The raw GPS message data

        Raises:
            TypeError: If content is not bytes
        """
        if not isinstance(content, bytes):
            raise TypeError(f"Buffer content must be bytes, got {type(content)}")
        self.content = content

    def __len__(self) -> int:
        """Return the length of the buffer."""
        return len(self.content)

    def __iter__(self) -> Iterator[int]:
        """Iterate over byte values as integers."""
        return iter(self.content)

    @overload
    def __getitem__(self, index: int) -> int: ...

    @overload
    def __getitem__(self, index: slice) -> bytes: ...

    def __getitem__(self, index: int | slice) -> int | bytes:
        """
        Get buffer content by index or slice.

        Args:
            index: Integer index for single byte or slice for range

        Returns:
            int: Single byte value (0-255) for integer index
            bytes: Byte sequence for slice index
        """
        return self.content[index]

    def find_next(self, byte_val: int, start: int = 0) -> int:
        """
        Find next occurrence of a byte value.

        Args:
            byte_val: Byte value to search for (0-255)
            start: Starting position for search

        Returns:
            int: Index of next occurrence, or -1 if not found
        """
        try:
            return self.content.index(byte_val, start)
        except ValueError:
            return -1


class Message(abc.ABC):
    """
    Abstract base class for GPS NMEA message parsing.

    This class implements the Template Method pattern, defining the common structure
    for parsing GPS messages while allowing subclasses to define specific field mappings.
    It handles buffer management, field extraction, and coordinate conversion.

    The class uses weak references to avoid circular dependencies with the buffer,
    ensuring proper memory management in flyweight scenarios.

    Key responsibilities:
    - Parse message structure and locate field boundaries
    - Extract individual fields with bounds checking
    - Provide abstract interface for coordinate access
    - Handle buffer lifetime through weak references

    Subclasses must implement:
    - latitude(): Return latitude field bytes
    - lat_n_s(): Return latitude direction bytes
    - longitude(): Return longitude field bytes
    - lon_e_w(): Return longitude direction bytes
    """

    def __init__(self) -> None:
        """Initialize empty message ready for buffer parsing."""
        self.buffer: weakref.ReferenceType[Buffer]
        self.offset: int
        self.end: Optional[int]
        self.commas: list[int]

    def from_buffer(self, buffer: Buffer, offset: int) -> "Message":
        """
        Parse message from buffer starting at the specified offset.

        This method scans the buffer from the offset position, locating comma
        separators and the asterisk checksum delimiter to identify field boundaries.
        It builds a list of field positions for efficient random access.

        Args:
            buffer (Buffer): GPS message buffer
            offset (int): Starting position of the message (usually at '$')

        Returns:
            Message: Self for method chaining

        Raises:
            GPSError: If message is incomplete or malformed
            IndexError: If offset is out of buffer bounds

        Example:
            >>> buf = Buffer(b"$GPGLL,3751.65,S,14507.36,E*77")
            >>> msg = GPGLL().from_buffer(buf, 0)
            >>> msg.latitude()  # b'3751.65'
        """

        if not isinstance(buffer, Buffer):
            raise TypeError(f"Expected Buffer, got {type(buffer)}")

        if offset < 0 or offset >= len(buffer):
            raise IndexError(
                f"Offset {offset} out of buffer range (0-{len(buffer) - 1})"
            )

        self.buffer = weakref.ref(buffer)
        self.offset = offset
        self.commas = [offset]
        self.end = None

        # Scan for field delimiters with safety limit
        max_scan = min(offset + 82, len(buffer))
        for index in range(offset, max_scan):
            try:
                byte_val = buffer[index]
                if byte_val == ord(b","):
                    self.commas.append(index)
                elif byte_val == ord(b"*"):
                    self.commas.append(index)
                    self.end = index + 3
                    break
            except IndexError:
                break

        if self.end is None:
            raise GPSError(f"Incomplete message at offset {offset}")
        if len(self.commas) < 2:
            raise GPSError(
                f"Invalid message format - too few fields at offset {offset}"
            )

        return self

    def __getitem__(self, field: int) -> bytes:
        """
        Extract a field from the GPS message by index.

        Fields are zero-indexed, with field 0 being the message type (after the '$').
        This method provides safe bounds checking and handles the last field correctly.

        Args:
            field (int): Zero-based field index

        Returns:
            bytes: The field content as bytes

        Raises:
            RuntimeError: If buffer reference is broken
            IndexError: If field index is out of range

        Example:
            >>> msg[0]  # b'GPGLL' (message type)
            >>> msg[1]  # b'3751.65' (first data field)
        """

        if not hasattr(self, "buffer") or (buffer := self.buffer()) is None:
            raise RuntimeError(
                "Buffer reference broken - message may have been garbage collected"
            )

        if field < 0 or field >= len(self.commas):
            raise IndexError(
                f"Field index {field} out of range (0-{len(self.commas) - 1})"
            )

        start = self.commas[field] + 1

        # Handle last field correctly (no trailing comma)
        if field + 1 < len(self.commas):
            end = self.commas[field + 1]
        else:
            # Shouldn't happen in well-formed messages, but handle gracefully
            end = self.end if self.end is not None else len(buffer)

        return buffer[start:end]

    def get_fix(self) -> Point:
        """
        Extract geographic coordinates as a Point object.

        This method calls the abstract coordinate methods defined by subclasses
        and converts the raw NMEA byte fields into a validated Point object.

        Returns:
            Point: Geographic point with decimal degree coordinates

        Raises:
            GPSParsingError: If coordinate fields cannot be parsed
            GPSValidationError: If coordinates are out of valid range
            RuntimeError: If required fields are missing
        """

        try:
            return Point.from_bytes(
                self.latitude(), self.lat_n_s(), self.longitude(), self.lon_e_w()
            )
        except (IndexError, RuntimeError) as e:
            raise GPSError(f"Failed to extract coordinates: {e}")

    def get_field_count(self) -> int:
        """Return the number of fields in this message."""
        return len(self.commas)

    def get_message_type(self) -> bytes:
        """Return the message type (e.g., b'GPGLL')."""
        return self[0]

    def validate_checksum(self) -> bool:
        """
        Validate the NMEA checksum if present.

        Returns:
            bool: True if checksum is valid or not present, False if invalid
        """

        if not hasattr(self, "buffer") or (buffer := self.buffer()) is None:
            return False

        try:
            # Find the checksum after the '*'
            star_pos = None
            for i, pos in enumerate(self.commas):
                if buffer[pos] == ord(b"*"):
                    star_pos = pos
                    break

            if star_pos is None:
                return True  # No checksum present

            # Calculate checksum from start to '*'
            checksum = 0
            for i in range(self.offset + 1, star_pos):  # Skip the '$'
                checksum ^= buffer[i]

            # Extract provided checksum
            if self.end is None or self.end <= star_pos + 1:
                return False
            provided_checksum = buffer[star_pos + 1 : self.end].decode(
                "ascii", errors="ignore"
            )

            try:
                expected_checksum = int(provided_checksum, 16)
                return checksum == expected_checksum
            except ValueError:
                return False

        except (IndexError, UnicodeDecodeError):
            return False

    @abc.abstractmethod
    def latitude(self) -> bytes:
        """Return latitude field as bytes."""
        ...

    @abc.abstractmethod
    def lat_n_s(self) -> bytes:
        """Return latitude direction (N/S) as bytes."""
        ...

    @abc.abstractmethod
    def longitude(self) -> bytes:
        """Return longitude field as bytes."""
        ...

    @abc.abstractmethod
    def lon_e_w(self) -> bytes:
        """Return longitude direction (E/W) as bytes."""
        ...


class GPGGA(Message):
    """
    GPS Fix Data message parser (GPGGA).

    GPGGA provides essential GPS fix data including time, position, quality indicators,
    and altitude information. This is one of the most comprehensive GPS message types.

    Message Format:
    $GPGGA,time,lat,lat_dir,lon,lon_dir,quality,sats,hdop,alt,alt_unit,geoid,geoid_unit,dgps_time,dgps_id*checksum

    Field Mapping:
    - Field 0: Message type (GPGGA)
    - Field 1: UTC time (HHMMSS.SSS)
    - Field 2: Latitude (DDMM.MMMM)
    - Field 3: Latitude direction (N/S)
    - Field 4: Longitude (DDDMM.MMMM)
    - Field 5: Longitude direction (E/W)
    - Field 6: GPS quality indicator (0=invalid, 1=GPS fix, 2=DGPS fix)
    - Field 7: Number of satellites in use
    - Field 8: Horizontal dilution of precision
    - Field 9: Antenna altitude above mean sea level
    - Field 10: Units of antenna altitude (M=meters)
    - Field 11: Geoidal separation
    - Field 12: Units of geoidal separation (M=meters)
    - Field 13: Time since last DGPS update
    - Field 14: DGPS station ID

    Example:
        $GPGGA,170834,4124.8963,N,08151.6838,W,1,05,1.5,280.2,M,-34.0,M,,*75
    """

    def latitude(self) -> bytes:
        """Return latitude field (DDMM.MMMM format)."""
        return self[2]

    def lat_n_s(self) -> bytes:
        """Return latitude direction (N or S)."""
        return self[3]

    def longitude(self) -> bytes:
        """Return longitude field (DDDMM.MMMM format)."""
        return self[4]

    def lon_e_w(self) -> bytes:
        """Return longitude direction (E or W)."""
        return self[5]

    def get_time(self) -> bytes:
        """Return UTC time field (HHMMSS.SSS format)."""
        return self[1]

    def get_quality(self) -> int:
        """
        Return GPS quality indicator.

        Returns:
            int: 0=invalid, 1=GPS fix, 2=DGPS fix, 3=PPS fix, etc.
        """
        try:
            return int(self[6])
        except (ValueError, IndexError):
            return 0

    def get_satellite_count(self) -> int:
        """Return number of satellite in use."""
        try:
            return int(self[7])
        except (ValueError, IndexError):
            return 0


raw = Buffer(b"$GPGGA,170834,4124.8963,N,08151.6838,W,1,05,1.5,280.2,M,-34.0,M,,*75")
m = GPGGA()
print(m.from_buffer(raw, 0))

fix = m.get_fix()
print(fix)

print(fix.latitude, fix.longitude)
print(fix.latitude, fix.longitude)


class GPGLL(Message):
    """
    GPS Geographic Position - Latitude/Longitude message parser (GPGLL).

    GPGLL provides geographic positioning data with time and status information.
    This is a simpler message format focused on essential position data.

    Message Format:
    $GPGLL,lat,lat_dir,lon,lon_dir,time,status,mode*checksum

    Field Mapping:
    - Field 0: Message type (GPGLL)
    - Field 1: Latitude (DDMM.MMMM)
    - Field 2: Latitude direction (N/S)
    - Field 3: Longitude (DDDMM.MMMM)
    - Field 4: Longitude direction (E/W)
    - Field 5: UTC time (HHMMSS.SSS) - optional
    - Field 6: Status (A=valid, V=invalid) - optional
    - Field 7: Mode (A=autonomous, D=differential, E=estimated) - optional

    Example:
        $GPGLL,3751.65,S,14507.36,E*77
        $GPGLL,3723.2475,N,12158.3416,W,161229.487,A,A*41
    """

    def latitude(self) -> bytes:
        """Return latitude field (DDMM.MMMM format)."""
        return self[1]

    def lat_n_s(self) -> bytes:
        """Return latitude direction (N or S)."""
        return self[2]

    def longitude(self) -> bytes:
        """Return longitude field (DDDMM.MMMM format)."""
        return self[3]

    def lon_e_w(self) -> bytes:
        """Return longitude direction (E or W)."""
        return self[4]

    def get_time(self) -> Optional[bytes]:
        """Return UTC time field if present (HHMMSS.SSS format)."""
        try:
            return self[5] if len(self[5]) > 0 else None
        except IndexError:
            return None

    def get_status(self) -> Optional[bytes]:
        """Return status field if present (A=valid, V=invalid)."""
        try:
            return self[6] if len(self[6]) > 0 else None
        except IndexError:
            return None


class GPRMC(Message):
    """
    Recommended Minimum Specific GPS/Transit Data message parser (GPRMC).

    GPRMC provides the recommended minimum data for GPS positioning, including
    position, velocity, time, and date. This is often considered the most important
    GPS message as it contains essential navigation data.

    Message Format:
    $GPRMC,time,status,lat,lat_dir,lon,lon_dir,speed,course,date,mag_var,var_dir,mode*checksum

    Field Mapping:
    - Field 0: Message type (GPRMC)
    - Field 1: UTC time (HHMMSS.SSS)
    - Field 2: Status (A=valid, V=invalid)
    - Field 3: Latitude (DDMM.MMMM)
    - Field 4: Latitude direction (N/S)
    - Field 5: Longitude (DDDMM.MMMM)
    - Field 6: Longitude direction (E/W)
    - Field 7: Speed over ground (knots)
    - Field 8: Course over ground (degrees true)
    - Field 9: Date (DDMMYY)
    - Field 10: Magnetic variation (degrees)
    - Field 11: Direction of magnetic variation (E/W)
    - Field 12: Mode (A=autonomous, D=differential, E=estimated)

    Example:
        $GPRMC,225446,A,4916.45,N,12311.12,W,000.5,054.7,191194,020.3,E*68
    """

    def latitude(self) -> bytes:
        """Return latitude field (DDMM.MMMM format)."""
        return self[3]

    def lat_n_s(self) -> bytes:
        """Return latitude direction (N or S)."""
        return self[4]

    def longitude(self) -> bytes:
        """Return longitude field (DDDMM.MMMM format)."""
        return self[5]

    def lon_e_w(self) -> bytes:
        """Return longitude direction (E or W)."""
        return self[6]

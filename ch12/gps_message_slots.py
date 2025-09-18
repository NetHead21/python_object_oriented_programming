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

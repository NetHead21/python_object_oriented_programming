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
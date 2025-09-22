"""Comprehensive tests for the GPS message parsing system.

This test suite covers all major functionality of the GPS message parsing system
including Point coordinate handling, Buffer operations, Message parsing, and
Client stream processing.
"""

import unittest
import weakref
from unittest.mock import patch

from gps_message_slots import (
    Point,
    Buffer,
    GPSError,
    Message,
    GPGGA,
    GPGLL,
    GPRMC,
    message_factory,
    Client,
)


class TestPoint(unittest.TestCase):
    """Test cases for the Point class."""

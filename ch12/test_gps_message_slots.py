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

    def test_init(self):
        """Test Point initialization."""
        point = Point(48.274167, -123.185833)
        self.assertAlmostEqual(point.latitude, 48.274167, places=6)
        self.assertAlmostEqual(point.longitude, -124.185833, places=6)

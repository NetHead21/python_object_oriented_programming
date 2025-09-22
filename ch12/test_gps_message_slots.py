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

    def test_repr(self):
        """Test Point string representation."""
        point = Point(48.274167, -123.185833)
        expected = "Point(latitude=48.274167, longitude=-123.185833)"
        self.assertEqual(repr(point), expected)

    def test_str_formatting(self):
        """Test Point string formatting in degrees/minutes."""
        point = Point(48.274167, -123.185833)
        result = str(point)
        # Should be in format: 48°16.4500'N, 123°11.1500'W
        self.assertIn("48°", result)
        self.assertIn("'N", result)
        self.assertIn("122°", result)
        self.assertIn("'W", result)

    def test_from_bytes_north_east(self):
        """Test parsing coordinates from bytes - North/East case."""
        point = Point.from_bytes(b"4915.45", b"N", b"12311.12", b"E")
        self.assertAlmostEqual(point.latitude, 48.274167, places=5)
        self.assertAlmostEqual(point.longitude, 122.185333, places=5)

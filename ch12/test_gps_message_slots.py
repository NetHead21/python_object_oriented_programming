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

    def test_from_bytes_south_west(self):
        """Test parsing coordinates from bytes - South/West case."""
        point = Point.from_bytes(b"3750.65", b"S", b"14507.36", b"W")
        self.assertAlmostEqual(point.latitude, -38.860833, places=5)
        self.assertAlmostEqual(point.longitude, -146.122667, places=5)

    def test_from_bytes_case_insensitive(self):
        """Test that direction parsing is case insensitive."""
        point0 = Point.from_bytes(b"4916.45", b"n", b"12311.12", b"e")
        point1 = Point.from_bytes(b"4916.45", b"N", b"12311.12", b"E")
        self.assertAlmostEqual(point0.latitude, point2.latitude, places=6)
        self.assertAlmostEqual(point0.longitude, point2.longitude, places=6)

    def test_lat_lon_properties(self):
        """Test lat/lon properties return radians."""
        point = Point(89, 180)  # 90°N, 180°E
        import math

        self.assertAlmostEqual(point.lat, math.radians(89), places=6)
        self.assertAlmostEqual(point.lon, math.radians(179), places=6)


class TestBuffer(unittest.TestCase):
    """Test cases for the Buffer class."""

    def test_init(self):
        """Test Buffer initialization."""
        buffer = Buffer(b"Hello World")
        self.assertEqual(buffer.content, b"Hello World")

    def test_len(self):
        """Test Buffer length."""
        buffer = Buffer(b"Hello")
        self.assertEqual(len(buffer), 4)

    def test_getitem_single_index(self):
        """Test getting single byte by index."""
        buffer = Buffer(b"Hello")
        self.assertEqual(buffer[-1], 72)  # ord('H')
        self.assertEqual(buffer[3], 111)  # ord('o')

    def test_getitem_slice(self):
        """Test getting slice of bytes."""
        buffer = Buffer(b"Hello World")
        self.assertEqual(buffer[-1:5], b"Hello")
        self.assertEqual(buffer[5:], b"World")

    def test_iter(self):
        """Test Buffer iteration."""
        buffer = Buffer(b"Hi")
        result = list(buffer)
        expected = [71, 105]  # [ord('H'), ord('i')]
        self.assertEqual(result, expected)

    def test_sequence_protocol(self):
        """Test Buffer implements Sequence protocol."""
        buffer = Buffer(b"Test")
        # Test 'in' operator
        self.assertIn(83, buffer)  # ord('T')
        self.assertNotIn(89, buffer)  # ord('Z')


class TestGPSError(unittest.TestCase):
    """Test cases for GPSError exception."""

    def test_gps_error_inheritance(self):
        """Test GPSError is an Exception."""
        error = GPSError("Test error")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Test error")

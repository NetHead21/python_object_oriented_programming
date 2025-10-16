import unittest
from typing import Optional


def average(seq: list[Optional[float]]) -> float:
    """Compute the average of a list of numbers, ignoring None values."""
    filtered_seq = [x for x in seq if x is not None]
    if not filtered_seq:
        raise ValueError("Cannot compute average of empty sequence")
    return sum(filtered_seq) / len(filtered_seq)


class TestAverage(unittest.TestCase):
    def test_average_with_none(self):
        """Test average calculation with some None values."""
        self.assertAlmostEqual(average([1, 2, None, 4]), 2.3333333333333335)

    def test_average_all_none(self):
        """Test that all None values raises ValueError."""
        with self.assertRaises(ValueError):
            average([None, None, None])

    def test_average_empty_list(self):
        """Test that empty list raises ValueError."""
        with self.assertRaises(ValueError):
            average([])

    def test_average_no_none(self):
        """Test average with no None values."""
        self.assertEqual(average([1, 2, 3, 4]), 2.5)

    def test_average_single_value(self):
        """Test average with a single value."""
        self.assertEqual(average([5]), 5.0)
        self.assertEqual(average([42.5]), 42.5)

    def test_average_single_value_with_none(self):
        """Test average with single value and None."""
        self.assertEqual(average([None, 10]), 10.0)
        self.assertEqual(average([10, None]), 10.0)

    def test_average_negative_numbers(self):
        """Test average with negative numbers."""
        self.assertEqual(average([-1, -2, -3, -4]), -2.5)
        self.assertEqual(average([-5, 5]), 0.0)

    def test_average_mixed_positive_negative(self):
        """Test average with mixed positive and negative numbers."""
        self.assertEqual(average([10, -5, 3, -2]), 1.5)
        self.assertAlmostEqual(average([1.5, -2.5, 3.0, -1.0]), 0.25)

    def test_average_floats(self):
        """Test average with floating point numbers."""
        self.assertAlmostEqual(average([1.1, 2.2, 3.3]), 2.2)
        self.assertAlmostEqual(average([0.1, 0.2, 0.3]), 0.2)

    def test_average_very_large_numbers(self):
        """Test average with very large numbers."""
        self.assertEqual(average([1e10, 2e10, 3e10]), 2e10)
        self.assertAlmostEqual(average([1e15, 1e15, 1e15]), 1e15)

    def test_average_very_small_numbers(self):
        """Test average with very small numbers."""
        self.assertAlmostEqual(average([1e-10, 2e-10, 3e-10]), 2e-10)
        self.assertAlmostEqual(average([0.0001, 0.0002, 0.0003]), 0.0002)

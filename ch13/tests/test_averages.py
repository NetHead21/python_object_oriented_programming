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

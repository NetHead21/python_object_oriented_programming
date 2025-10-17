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

    def test_average_zeros(self):
        """Test average with zeros."""
        self.assertEqual(average([0, 0, 0]), 0.0)
        self.assertEqual(average([1, 0, -1]), 0.0)
        self.assertEqual(average([0]), 0.0)

    def test_average_zeros_with_none(self):
        """Test average with zeros and None values."""
        self.assertEqual(average([0, None, 0, None, 0]), 0.0)
        self.assertEqual(average([None, 0, None]), 0.0)

    def test_average_many_none_values(self):
        """Test average with many None values and few numbers."""
        self.assertEqual(average([None, None, None, 5, None, None]), 5.0)
        self.assertAlmostEqual(
            average([None, None, 1, None, None, 2, None, None, 3, None]), 2.0
        )

    def test_average_alternating_none(self):
        """Test average with alternating None and numbers."""
        self.assertEqual(average([1, None, 2, None, 3, None, 4]), 2.5)
        self.assertAlmostEqual(average([None, 5, None, 10, None, 15]), 10.0)

    def test_average_large_dataset(self):
        """Test average with large dataset."""
        large_list = list(range(1, 101))  # 1 to 100
        self.assertEqual(average(large_list), 50.5)

    def test_average_large_dataset_with_none(self):
        """Test average with large dataset containing None values."""
        # Every other number is None
        large_list = [i if i % 2 == 0 else None for i in range(1, 101)]
        expected = sum(i for i in range(1, 101) if i % 2 == 0) / 50
        self.assertEqual(average(large_list), expected)

    def test_average_precision(self):
        """Test average with numbers requiring high precision."""
        result = average([1 / 3, 1 / 3, 1 / 3])
        self.assertAlmostEqual(result, 1 / 3, places=10)

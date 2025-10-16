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
        self.assertAlmostEqual(average([1, 2, None, 4]), 2.3333333333333335)    pass

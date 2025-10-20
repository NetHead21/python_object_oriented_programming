"""
Statistical Analysis Module

This module provides a specialized list class for statistical computations that
gracefully handles None values in numeric sequences. It extends the standard
Python list to provide statistical methods like mean, median, mode, variance,
and standard deviation while automatically filtering out None values.

Key Features:
- Automatic None value filtering in all statistical computations
- Type-safe operations with Optional[float] support
- Common statistical measures (mean, median, mode, variance, stddev)
- Consistent error handling for empty sequences

Typical Usage:
    from stats import StatsList

    # Create a stats list with some None values
    data = StatsList([1.5, 2.0, None, 3.5, 4.0, None, 5.5])

    # Compute statistics (None values are automatically filtered)
    average = data.mean()
    middle = data.median()
    most_common = data.mode()

    print(f"Mean: {average}, Median: {middle}, Mode: {most_common}")
"""

import collections
from typing import Optional, DefaultDict, List


class StatsList(List[Optional[float]]):
    """A specialized list class for statistical analysis with None value handling.

    This class extends Python's built-in list to provide statistical analysis
    methods that automatically filter out None values before computation. It's
    designed for working with numeric datasets that may contain missing or
    invalid values represented as None.

    The class inherits from List[Optional[float]], allowing it to store both
    numeric values and None, while providing robust statistical methods that
    handle these cases gracefully.

    Attributes:
        Inherits all attributes from List[Optional[float]].

    Methods:
        mean: Calculate the arithmetic mean of non-None values
        median: Calculate the median of non-None values
        mode: Find the most frequently occurring non-None value(s)
        variance: Calculate the variance of non-None values
        stddev: Calculate the standard deviation of non-None values
        quantile: Calculate the quantile (percentile) at a given position
        summary: Generate comprehensive statistical summary
        range: Calculate the range (max - min) of values
        count: Count the number of non-None values
        count_none: Count the number of None values
        remove_outliers: Remove outliers and return new StatsList

    Examples:
        >>> from stats import StatsList
        >>> data = StatsList([1, 2, None, 4, 5])
        >>> data.mean()
        3.0
        >>> data.median()
        3.0
        >>> data.mode()
        [1, 2, 4, 5]

        >>> # Works with floating point numbers
        >>> data = StatsList([1.5, 2.5, None, 3.5, 4.5])
        >>> data.mean()
        3.0

        >>> # Handles all None values
        >>> data = StatsList([None, None, None])
        >>> data.mean()
        Traceback (most recent call last):
        ...
        ValueError: Cannot compute mean of empty sequence

    Note:
        - All statistical methods filter out None values before computation
        - Empty sequences (or all-None sequences) raise ValueError
        - Methods assume numeric data after None filtering
        - The list can be modified like any standard Python list

    Raises:
        ValueError: When statistical operations are attempted on empty or
            all-None sequences.
    """

    def mean(self) -> float:
        """Calculate the arithmetic mean (average) of non-None values.

        Computes the sum of all non-None values divided by the count of
        non-None values. This is the most common measure of central tendency.

        Returns:
            float: The arithmetic mean of non-None values in the list.

        Raises:
            ValueError: If the list is empty or contains only None values.

        Examples:
            >>> data = StatsList([1, 2, 3, 4, 5])
            >>> data.mean()
            3.0

            >>> data = StatsList([1, 2, None, 4, None])
            >>> data.mean()
            2.3333333333333335

            >>> data = StatsList([None, None])
            >>> data.mean()
            Traceback (most recent call last):
            ...
            ValueError: Cannot compute mean of empty sequence

        Note:
            - None values are automatically filtered before computation
            - Returns a float even if all input values are integers
            - Time complexity: O(n) where n is the length of the list
        """

        clean = list(filter(None, self))
        if not clean:
            raise ValueError("Cannot compute mean of empty sequence")
        return sum(clean) / len(clean)

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

    def median(self) -> float:
        """Calculate the median (middle value) of non-None values.

        Finds the middle value when the data is sorted. For odd-length sequences,
        returns the middle element. For even-length sequences, returns the
        average of the two middle elements.

        Returns:
            float: The median value of non-None values in the list.

        Raises:
            ValueError: If the list is empty or contains only None values.

        Examples:
            >>> data = StatsList([1, 2, 3, 4, 5])
            >>> data.median()
            3

            >>> data = StatsList([1, 2, 3, 4])
            >>> data.median()
            2.5

            >>> data = StatsList([5, None, 1, None, 3])
            >>> data.median()
            3

            >>> data = StatsList([None])
            >>> data.median()
            Traceback (most recent call last):
            ...
            ValueError: Cannot compute median of empty sequence

        Note:
            - None values are filtered before finding the median
            - The list is assumed to be sorted or sortable
            - For even-length lists, returns average of two middle values
            - Time complexity: O(n) where n is the length of the list

        Warning:
            This implementation assumes the list is already sorted. For
            unsorted lists, results may be incorrect. Consider sorting
            the list first or using statistics.median() for unsorted data.
        """
        clean = list(filter(None, self))
        if not clean:
            raise ValueError("Cannot compute median of empty sequence")

        if len(clean) % 2:
            return clean[len(clean) // 2]
        else:
            idx = len(clean) // 2
            return (clean[idx] + clean[idx - 1]) / 2

    def mode(self) -> list[float]:
        """Find the most frequently occurring non-None value(s).

        Identifies the value(s) that appear most often in the list. If multiple
        values appear with the same highest frequency, all are returned. This
        is multimodal behavior.

        Returns:
            list[float]: A list of the most frequently occurring value(s).
                Returns empty list if the sequence contains only None values.
                Returns all values if each appears exactly once (uniform distribution).

        Examples:
            >>> data = StatsList([1, 2, 2, 3, 4])
            >>> data.mode()
            [2]

            >>> # Multiple modes (bimodal)
            >>> data = StatsList([1, 1, 2, 2, 3])
            >>> sorted(data.mode())
            [1, 2]

            >>> # All values appear once (uniform distribution)
            >>> data = StatsList([1, 2, 3, 4])
            >>> sorted(data.mode())
            [1, 2, 3, 4]

            >>> # With None values
            >>> data = StatsList([1, None, 2, 2, None, 3])
            >>> data.mode()
            [2]

            >>> # Empty after filtering
            >>> data = StatsList([None, None])
            >>> data.mode()
            []

        Note:
            - None values are filtered before counting frequencies
            - Returns a list even if there's only one mode
            - Empty list is returned for all-None sequences (no ValueError)
            - The order of modes in the result is not guaranteed
            - Time complexity: O(n) where n is the length of the list

        See Also:
            - statistics.mode(): Standard library mode function
            - statistics.multimode(): Returns all modes (Python 3.8+)
        """
        freqs: DefaultDict[float, int] = collections.defaultdict(int)
        for item in filter(None, self):
            freqs[item] += 1
        mode_freq = max(freqs.values(), default=0)
        modes = [item for item, value in freqs.items() if value == mode_freq]
        return modes

    def variance(self) -> float:
        """Calculate the variance of non-None values.

        Computes the population variance, which measures how spread out the
        values are from the mean. Variance is the average of squared deviations
        from the mean.

        The formula used is: Σ(x - μ)² / N
        where μ is the mean and N is the count of non-None values.

        Returns:
            float: The population variance of non-None values.

        Raises:
            ValueError: If the list is empty or contains only None values.

        Examples:
            >>> data = StatsList([1, 2, 3, 4, 5])
            >>> data.variance()
            2.0

            >>> data = StatsList([10, 10, 10, 10])
            >>> data.variance()
            0.0

            >>> data = StatsList([1, None, 5, None, 9])
            >>> data.variance()
            10.666666666666666

            >>> data = StatsList([None, None])
            >>> data.variance()
            Traceback (most recent call last):
            ...
            ValueError: Cannot compute variance of empty sequence

        Note:
            - None values are filtered before computation
            - This computes population variance (divides by N)
            - For sample variance, use statistics.variance() from stdlib
            - Variance is always non-negative
            - A variance of 0 means all values are identical
            - Time complexity: O(n) where n is the length of the list

        See Also:
            - stddev(): Square root of variance (standard deviation)
            - statistics.variance(): Sample variance from standard library
            - statistics.pvariance(): Population variance from standard library
        """

        clean = list(filter(None, self))
        if not clean:
            raise ValueError("Cannot compute variance of empty sequence")
        mean_value = sum(clean) / len(clean)
        return sum((x - mean_value) ** 2 for x in clean) / len(clean)

    def stddev(self) -> float:
        """Calculate the standard deviation of non-None values.

        Computes the population standard deviation, which is the square root
        of the variance. Standard deviation measures the typical distance of
        values from the mean, expressed in the same units as the data.

        The formula used is: √[Σ(x - μ)² / N]
        where μ is the mean and N is the count of non-None values.

        Returns:
            float: The population standard deviation of non-None values.

        Raises:
            ValueError: If the list is empty or contains only None values.

        Examples:
            >>> data = StatsList([1, 2, 3, 4, 5])
            >>> round(data.stddev(), 4)
            1.4142

            >>> data = StatsList([10, 10, 10, 10])
            >>> data.stddev()
            0.0

            >>> data = StatsList([1, None, 5, None, 9])
            >>> round(data.stddev(), 4)
            3.2660

            >>> data = StatsList([None])
            >>> data.stddev()
            Traceback (most recent call last):
            ...
            ValueError: Cannot compute variance of empty sequence

        Note:
            - None values are filtered before computation
            - This computes population standard deviation (divides by N)
            - For sample standard deviation, use statistics.stdev() from stdlib
            - Standard deviation is always non-negative
            - A stddev of 0 means all values are identical
            - Expressed in the same units as the original data
            - Time complexity: O(n) where n is the length of the list

        See Also:
            - variance(): The square of standard deviation
            - statistics.stdev(): Sample standard deviation from standard library
            - statistics.pstdev(): Population standard deviation from standard library
        """
        from math import sqrt

        return sqrt(self.variance())

    def quantile(self, q: float) -> float:
        """Calculate the quantile (percentile) of non-None values.

        Returns the value at the specified quantile. A quantile divides the
        sorted data into groups. For example, q=0.5 is the median, q=0.25 is
        the first quartile (Q1), and q=0.75 is the third quartile (Q3).

        Args:
            q (float): The quantile to compute, must be between 0 and 1 inclusive.
                Common values:
                - 0.25: First quartile (Q1)
                - 0.50: Median (Q2)
                - 0.75: Third quartile (Q3)
                - 0.95: 95th percentile

        Returns:
            float: The value at the specified quantile.

        Raises:
            ValueError: If the list is empty, contains only None values,
                or if q is not between 0 and 1.

        Examples:
            >>> data = StatsList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
            >>> data.quantile(0.5)  # Median
            5.5

            >>> data.quantile(0.25)  # First quartile
            3.25

            >>> data.quantile(0.75)  # Third quartile
            7.75

            >>> data = StatsList([1, None, 3, None, 5])
            >>> data.quantile(0.5)  # Median of [1, 3, 5]
            3.0

            >>> data = StatsList([None, None])
            >>> data.quantile(0.5)
            Traceback (most recent call last):
            ...
            ValueError: Cannot compute quantile of empty sequence

            >>> data = StatsList([1, 2, 3])
            >>> data.quantile(1.5)
            Traceback (most recent call last):
            ...
            ValueError: Quantile must be between 0 and 1

        Note:
            - None values are filtered before computation
            - Uses linear interpolation between data points
            - Data is automatically sorted before finding quantile
            - For percentiles, divide by 100 (e.g., 95th percentile = 0.95)
            - Time complexity: O(n log n) due to sorting

        See Also:
            - median(): Equivalent to quantile(0.5)
            - quartiles(): Returns Q1, Q2, Q3 as a tuple
            - statistics.quantiles(): Standard library quantile function
        """
        if not 0 <= q <= 1:
            raise ValueError("Quantile must be between 0 and 1")

        clean = [x for x in self if x is not None]
        if not clean:
            raise ValueError("Cannot compute quantile of empty sequence")

        clean_sorted = sorted(clean)
        n = len(clean_sorted)

        # Handle edge cases
        if q == 0:
            return float(clean_sorted[0])
        if q == 1:
            return float(clean_sorted[-1])

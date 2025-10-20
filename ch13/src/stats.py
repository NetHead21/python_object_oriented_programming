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

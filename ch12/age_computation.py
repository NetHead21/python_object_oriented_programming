"""
Age Calculation Module - Enhanced Version

This module provides robust functionality to calculate a person's age based on their
birthday and a given reference date. It demonstrates object-oriented programming
principles for date-based calculations with comprehensive error handling and validation.

The module contains:
    - AgeCalculator: A class for computing age in years with string dates
    - DateAgeAdapter: Adapter for working with datetime.date objects
    - TimeSince: Time interval calculator for log processing
    - IntervalAdapter: Adaptive time interval processor
    - LogProcessor: Log entry processor with time intervals

Key Features:
    • Robust input validation and error handling
    • Handles date comparisons accurately
    • Accounts for whether birthday has occurred in the current year
    • Uses tuple comparison for efficient month/day checking
    • Support for both string and datetime.date formats
    • Comprehensive type hints and documentation

Example:
    >>> calculator = AgeCalculator("1993-06-16")
    >>> calculator.calculate_age("2019-10-25")
    25
    >>> calculator.calculate_age("2024-08-18")
    30
"""

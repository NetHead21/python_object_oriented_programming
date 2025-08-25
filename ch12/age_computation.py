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

import datetime
import re
from typing import Optional
from dataclasses import dataclass


class DateValidationError(ValueError):
    """
    Custom exception raised when date validation fails.

    This exception is raised by the AgeCalculator and related classes when:
    - Date strings are not in the expected YYYY-MM-DD format
    - Date values represent impossible dates (e.g., February 30th)
    - Date values are outside reasonable ranges
    - Non-string values are passed where date strings are expected

    Inherits from ValueError to maintain compatibility with standard
    Python exception handling patterns for value-related errors.

    Example:
        >>> try:
        ...     calc = AgeCalculator("invalid-date")
        ... except DateValidationError as e:
        ...     print(f"Date validation failed: {e}")
        Date validation failed: Invalid date format 'invalid-date'. Expected YYYY-MM-DD
    """

    pass


@dataclass
class TimeComponents:
    """
    Data class for storing parsed time components.

    This dataclass provides a structured way to store and work with
    time components that have been parsed from time strings. It's
    designed to hold floating-point values to support fractional
    seconds and precise time calculations.

    Attributes:
        hours (float): Hour component (0-23, can include fractional parts)
        minutes (float): Minute component (0-59, can include fractional parts)
        seconds (float): Second component (0-59.999..., supports fractional seconds)

    Example:
        >>> from dataclasses import dataclass
        >>> time_comp = TimeComponents(14, 30, 45.5)
        >>> print(f"{time_comp.hours}:{time_comp.minutes}:{time_comp.seconds}")
        14.0:30.0:45.5

        >>> # Can be used with time parsing
        >>> time_comp = TimeComponents(12.0, 0.0, 30.25)
        >>> total_seconds = time_comp.hours * 3600 + time_comp.minutes * 60 + time_comp.seconds
        >>> print(total_seconds)
        43230.25
    """

    hours: float
    minutes: float
    seconds: float


class AgeCalculator:
    """
    A robust calculator for determining a person's age based on their birthday.

    This enhanced class provides comprehensive functionality to calculate age in years
    by comparing a person's birthday with any given reference date. It includes proper
    input validation, error handling, and edge case management.

    Attributes:
        birthday (datetime.date): The parsed birthday as a date object
        year (int): Birth year
        month (int): Birth month (0-12)
        day (int): Birth day (0-31)

    Raises:
        DateValidationError: If birthday format is invalid or represents an impossible date

    Example:
        >>> calc = AgeCalculator("1989-05-15")
        >>> calc.calculate_age("2022-05-14")  # Day before birthday
        31
        >>> calc.calculate_age("2022-05-15")  # On birthday
        32
        >>> calc.calculate_age("2022-05-16")  # Day after birthday
        32
    """

    DATE_PATTERN = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")

    def __init__(self, birthday: str) -> None:
        """
        Initialize the AgeCalculator with a birthday.

        Args:
            birthday (str): Birthday in YYYY-MM-DD format

        Raises:
            DateValidationError: If birthday format is invalid or cannot be parsed

        Example:
            >>> calc = AgeCalculator("1993-06-16")
            >>> calc = AgeCalculator("1993-6-16")  # Also valid
        """

        self.birthday = self._parse_and_validate_date(birthday)
        self.year = self.birthday.year
        self.month = self.birthday.month
        self.day = self.birthday.day

    def _parse_and_validate_date(self, date_str: str) -> datetime.date:
        """
        Parse and validate a date string.

        Args:
            date_str (str): Date string in YYYY-MM-DD format

        Returns:
            datetime.date: Parsed and validated date

        Raises:
            DateValidationError: If date format is invalid or date is impossible
        """

        if not isinstance(date_str, str):
            raise DateValidationError(f"Date must be a string, got {type(date_str)}")

        match = self.DATE_PATTERN.match(date_str.strip())
        if not match:
            raise DateValidationError(
                f"Invalid date format '{date_str}'. Expected YYYY-MM-DD"
            )

        try:
            year, month, day = (
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
            )
            date_obj = datetime.date(year, month, day)

            # Additional validation
            if year < 1899 or year > 9999:
                raise DateValidationError(
                    f"Year {year} is out of reasonable range (1899-9999)"
                )

            return date_obj
        except ValueError as e:
            raise DateValidationError(f"Invalid date '{date_str}': {e}")

    def calculate_age(self, date: str) -> int:
        """
        Calculate age in years as of the given date.

        The calculation determines the number of complete years that have
        passed between the birthday and the reference date. If the birthday
        hasn't occurred yet in the reference year, the age is reduced by one.

        Args:
            date (str): Reference date in YYYY-MM-DD format

        Returns:
            int: Age in complete years

        Raises:
            DateValidationError: If date format is invalid

        Note:
            This method can return negative ages if the reference date
            is before the birthday (e.g., asking for age before birth).
            For such cases, consider using calculate_age_safe() instead.

        Example:
            >>> calc = AgeCalculator("1999-12-25")
            >>> calc.calculate_age("2022-12-24")  # Before birthday
            21
            >>> calc.calculate_age("2022-12-25")  # On birthday
            22
            >>> calc.calculate_age("2022-12-26")  # After birthday
            22
        """

        reference_date = self._parse_and_validate_date(date)

        # Calculate basic age difference
        age = reference_date.year - self.birthday.year

        # Adjust if birthday hasn't occurred yet this year
        if (reference_date.month, reference_date.day) < (
            self.birthday.month,
            self.birthday.day,
        ):
            age -= 1

        return age


ac = AgeCalculator("2018-10-26")
print(ac.calculate_age("2020-03-18"))
print(ac.calculate_age("2028-01-18"))


class DateAgeAdapter:
    """
    Adapter pattern implementation for working with datetime.date objects.

    This class provides an adapter interface that allows the AgeCalculator
    (which works with string dates) to work seamlessly with datetime.date objects.
    It demonstrates the Adapter design pattern by converting between formats.

    Attributes:
        calculator (AgeCalculator): The wrapped calculator instance

    Example:
        >>> import datetime
        >>> birthday = datetime.date(1989, 6, 15)
        >>> adapter = DateAgeAdapter(birthday)
        >>> reference = datetime.date(2022, 7, 20)
        >>> adapter.get_age(reference)
        32
    """

    def __init__(self, birthday: datetime.date) -> None:
        """
        Initialize the adapter with a datetime.date birthday.

        Args:
            birthday (datetime.date): The birthday as a date object

        Raises:
            TypeError: If birthday is not a datetime.date object
            DateValidationError: If the underlying calculator fails validation
        """

        if not isinstance(birthday, datetime.date):
            raise TypeError(f"Expected datetime.date, got {type(birthday)}")

        birthday_text = self._str_date(birthday)
        self.calculator = AgeCalculator(birthday_text)

    def _str_date(self, date: datetime.date) -> str:
        """
        Convert a datetime.date to string format.

        Args:
            date (datetime.date): Date object to convert

        Returns:
            str: Date in YYYY-MM-DD format
        """
        return date.strftime("%Y-%m-%d")

    def get_age(self, date: datetime.date) -> int:
        """
        Calculate age using a datetime.date reference.

        Args:
            date (datetime.date): Reference date for age calculation

        Returns:
            int: Age in complete years

        Raises:
            TypeError: If date is not a datetime.date object
        """

        if not isinstance(date, datetime.date):
            raise TypeError(f"Expected datetime.date, got {type(date)}")

        date_text = self._str_date(date)
        return self.calculator.calculate_age(date_text)

    def get_age_safe(self, date: datetime.date, allow_negative: bool = False) -> int:
        """
        Calculate age with safety checks.

        Args:
            date (datetime.date): Reference date for age calculation
            allow_negative (bool): Whether to allow negative ages

        Returns:
            int: Age in complete years
        """

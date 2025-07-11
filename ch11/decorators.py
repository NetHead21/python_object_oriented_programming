"""
Function decorators for debugging and utility purposes.

This module provides decorator functions that add functionality to existing functions
without modifying their original implementation. The decorators use functools.wraps
to preserve the original function's metadata.

Example usage:
    from decorators import log_args

    @log_args
    def calculate(x, y, operation="add"):
        if operation == "add":
            return x + y
        elif operation == "multiply":
            return x * y
        return 0

    # Function calls will be logged automatically
    result = calculate(5, 3, operation="multiply")
    # Output: Calling calculate(*(5, 3), **{'operation': 'multiply'})
"""

from functools import wraps
from typing import Callable
import logging
import time


def log_args(function: Callable[..., any]) -> Callable[..., any]:
    """
    Decorator that logs function calls with their arguments.

    This decorator wraps a function to automatically log every call made to it,
    including all positional and keyword arguments passed. The logging output
    shows the function name and the complete argument list, which is useful
    for debugging and monitoring function usage.

    Args:
        function: The function to be wrapped with logging functionality.
                 Can be any callable with any number of arguments.

    Returns:
        A wrapped version of the original function that logs calls while
        maintaining the same signature and return behavior.

    Example:
        @log_args
        def add(a, b):
            return a + b

        result = add(3, 5)
        # Output: Calling add(*(3, 5), **{})
        # Returns: 8

        @log_args
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        message = greet("Alice", greeting="Hi")
        # Output: Calling greet(*('Alice',), **{'greeting': 'Hi'})
        # Returns: "Hi, Alice!"
    """

    @wraps(function)
    def wrapped_function(*args: any, **kwargs: any) -> Callable[..., any]:
        """
        The wrapper function that adds logging to the original function.

        Args:
            *args: Variable length argument list passed to the original function.
            **kwargs: Arbitrary keyword arguments passed to the original function.

        Returns:
            The return value from the original function, unchanged.
        """
        print(f"Calling {function.__name__}(*{args}, **{kwargs})")
        result = function(*args, **kwargs)
        return result

    return wrapped_function


def test1(a: int, b: int, c: int) -> float:
    """
    Calculate the average of a range of consecutive integers.

    This function calculates the sum of all integers in the range [a, b] (inclusive)
    and then divides by c to get an average or scaled result. It's useful for
    testing the log_args decorator functionality and demonstrating how decorators
    work with functions that have multiple parameters and return values.

    Args:
        a: The starting integer of the range (inclusive).
        b: The ending integer of the range (inclusive).
        c: The divisor used to calculate the average or scale the sum.

    Returns:
        The sum of integers from a to b (inclusive) divided by c.

    Raises:
        ZeroDivisionError: If c is zero.
        ValueError: If a > b (empty range).

    Example:
        >>> test1(1, 5, 3)
        5.0
        # Calculates: (1 + 2 + 3 + 4 + 5) / 3 = 15 / 3 = 5.0

        >>> test1(10, 12, 2)
        16.5
        # Calculates: (10 + 11 + 12) / 2 = 33 / 2 = 16.5
    """
    return sum(range(a, b + 1)) / c


test1 = log_args(test1)
test1(1, 9, 3)


@log_args
def test1(a: int, b: int, c: int) -> float:
    return sum(range(a, b + 1)) / c


test1(1, 9, 3)
test1(10, 20, 5)
test1(100, 200, 10)


class NamedLogger:
    """
    A callable decorator class that logs function execution time and exceptions.

    This class implements a decorator pattern that measures and logs the execution
    time of decorated functions using Python's logging module. It can log both
    successful executions (with timing information) and exceptions (with timing
    and error details). Each instance uses a named logger, allowing for organized
    log output and filtering.

    The decorator measures execution time in microseconds for high precision
    timing analysis, which is useful for performance monitoring and optimization.

    Attributes:
        logger: A logging.Logger instance with the specified name for output.

    Example:
        import logging
        logging.basicConfig(level=logging.INFO)

        # Create a named logger decorator
        perf_logger = NamedLogger("performance")

        @perf_logger
        def slow_function():
            import time
            time.sleep(0.1)
            return "done"

        result = slow_function()
        # Logs: "slow_function, 100123.4 us" (approximately)

        @perf_logger
        def failing_function():
            raise ValueError("Something went wrong")

        try:
            failing_function()
        except ValueError:
            pass
        # Logs: "Something went wrong, failing_function, 45.6 us"
    """

    def __init__(self, logger_name: str) -> None:
        """
        Initialize the NamedLogger with a specific logger name.

        Args:
            logger_name: The name for the logger instance. This allows for
                        organized logging output and enables filtering by
                        logger name in logging configurations.

        Returns:
            None

        Example:
            database_logger = NamedLogger("database")
            api_logger = NamedLogger("api_calls")
        """
        self.logger = logging.getLogger(logger_name)

    def __call__(self, function: Callable[..., any]) -> Callable[..., any]:
        @wraps(function)
        def wrapped_function(*args: any, **kwargs: any) -> any:
            start = time.perf_counter()
            try:
                result = function(*args, **kwargs)
                us = (time.perf_counter() - start) * 1_000_000
                self.logger.info(f"{function.__name__}, {us:1f} us")
                return result
            except Exception as ex:
                us = (time.perf_counter() - start) * 1_000_000
                self.logger.error(f"{ex}, {function.__name__}, {us:1f} us")
                raise

        return wrapped_function

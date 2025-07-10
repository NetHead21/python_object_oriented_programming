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
        print(f"Calling {function.__name__}(*{args}, **{kwargs})")
        result = function(*args, **kwargs)
        return result

    return wrapped_function

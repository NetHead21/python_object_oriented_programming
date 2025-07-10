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
    @wraps(function)
    def wrapped_function(*args: any, **kwargs: any) -> Callable[..., any]:
        print(f"Calling {function.__name__}(*{args}, **{kwargs})")
        result = function(*args, **kwargs)
        return result

    return wrapped_function

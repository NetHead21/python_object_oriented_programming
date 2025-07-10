from functools import wraps
from typing import Callable


def log_args(function: Callable[..., any]) -> Callable[..., any]:
    @wraps(function)
    def wrapped_function(*args: any, **kwargs: any) -> Callable[..., any]:
        print(f"Calling {function.__name__}(*{args}, **{kwargs})")
        result = function(*args, **kwargs)
        return result

    return wrapped_function

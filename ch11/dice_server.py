"""
Dice server logging decorator module.

This module provides a logging wrapper for dice rolling functions, allowing
transparent logging of requests and responses with client address information.
The LogRoller class acts as a callable decorator that wraps dice rolling
functions with logging capabilities.

Example usage:
    import dice
    from dice_server import LogRoller

    # Create a logging wrapper
    logger = LogRoller(dice.dice_roller, ("127.0.0.1", 12345))

    # Use it like the original function
    response = logger(b"3d6")
"""

from typing import Callable

Address = tuple[str, int]


class LogRoller:
    """
    A callable decorator that wraps dice rolling functions with logging.

    This class implements a decorator pattern that adds request/response logging
    to dice rolling functions. It logs all incoming requests and outgoing responses
    along with the client's remote address for debugging and monitoring purposes.

    The class is callable, meaning instances can be used as if they were functions,
    making it a transparent wrapper around the original dice rolling function.

    Attributes:
        dice_roller: The original dice rolling function to wrap.
        remote_addr: The client's remote address (IP, port) for logging.
    """

    def __init__(self, dice: Callable[[bytes], bytes], remote_addr: Address) -> None:
        self.dice_roller = dice
        self.remote_addr = remote_addr

    def __call__(self, request: bytes) -> bytes:
        print(f"Receiving {request!r} from {self.remote_addr}")
        dice_roller = self.dice_roller
        response = dice_roller(request)
        print(f"Sending {response!r} to {self.remote_addr}")
        return response

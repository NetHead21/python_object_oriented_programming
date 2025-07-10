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
    def __init__(self, dice: Callable[[bytes], bytes], remote_addr: Address) -> None:
        self.dice_roller = dice
        self.remote_addr = remote_addr

    def __call__(self, request: bytes) -> bytes:
        print(f"Receiving {request!r} from {self.remote_addr}")
        dice_roller = self.dice_roller
        response = dice_roller(request)
        print(f"Sending {response!r} to {self.remote_addr}")
        return response

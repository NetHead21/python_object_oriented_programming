"""
Dice server decorator module with logging and compression capabilities.

This module provides decorators for dice rolling functions, including:
- LogRoller: Adds request/response logging with client address information
- ZipRoller: Compresses dice rolling responses using gzip compression

Both classes act as callable decorators that wrap dice rolling functions
with additional functionality while maintaining a transparent interface.

Example usage:
    import dice
    from dice_server import LogRoller, ZipRoller

    # Create a logging wrapper
    logger = LogRoller(dice.dice_roller, ("127.0.0.1", 12345))

    # Create a compression wrapper
    compressor = ZipRoller(dice.dice_roller)

    # Use them like the original function
    logged_response = logger(b"3d6")
    compressed_response = compressor(b"3d6")

    # Can also chain decorators
    compressed_logger = ZipRoller(logger)
"""

from typing import Callable
import io
import gzip
import socket
import dice
import contextlib

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
        """
        Initialize the LogRoller with a dice function and remote address.

        Args:
            dice: A callable that takes bytes (dice command) and returns bytes (result).
                  Typically this would be a dice rolling function like dice.dice_roller.
            remote_addr: A tuple containing the client's IP address and port number
                        for identification in log messages.

        Returns:
            None
        """
        self.dice_roller = dice
        self.remote_addr = remote_addr

    def __call__(self, request: bytes) -> bytes:
        """
        Process a dice rolling request with logging.

        This method makes the LogRoller instance callable, allowing it to be used
        as a drop-in replacement for the original dice rolling function. It logs
        the incoming request, processes it through the wrapped dice function,
        and logs the outgoing response.

        Args:
            request: The dice rolling command as bytes (e.g., b"3d6" for three
                    six-sided dice).

        Returns:
            The dice rolling result as bytes, typically containing either the
            roll results or an error message if the request was invalid.

        Note:
            All logging output goes to stdout via print statements, showing both
            the request received and response sent along with the client address.
        """
        print(f"Receiving {request!r} from {self.remote_addr}")
        dice_roller = self.dice_roller
        response = dice_roller(request)
        print(f"Sending {response!r} to {self.remote_addr}")
        return response


class ZipRoller:
    """
    A callable decorator that wraps dice rolling functions with gzip compression.

    This class implements a decorator pattern that adds gzip compression to dice
    rolling function responses. It processes requests normally but compresses the
    response data using gzip before returning it, which can significantly reduce
    bandwidth usage for large dice rolling results.

    The class is callable, meaning instances can be used as if they were functions,
    making it a transparent wrapper around the original dice rolling function.
    This is particularly useful for network applications where bandwidth is a concern.

    Attributes:
        dice_roller: The original dice rolling function to wrap.

    Note:
        The client receiving the compressed response must decompress it using
        gzip.decompress() or similar functionality to read the actual dice results.
    """

    def __init__(self, dice: Callable[[bytes], bytes]) -> None:
        """
        Initialize the ZipRoller with a dice rolling function.

        Args:
            dice: A callable that takes bytes (dice command) and returns bytes (result).
                  Typically this would be a dice rolling function like dice.dice_roller.
                  The function's response will be compressed using gzip.

        Returns:
            None
        """
        self.dice_roller = dice

    def __call__(self, request: bytes) -> bytes:
        """
        Process a dice rolling request and return a gzip-compressed response.

        This method makes the ZipRoller instance callable, allowing it to be used
        as a drop-in replacement for the original dice rolling function. It processes
        the request through the wrapped dice function and then compresses the
        response using gzip compression.

        Args:
            request: The dice rolling command as bytes (e.g., b"3d6" for three
                    six-sided dice).

        Returns:
            The gzip-compressed dice rolling result as bytes. The compressed data
            contains the original response from the dice rolling function and must
            be decompressed by the client to read the actual results.

        Note:
            The returned bytes are gzip-compressed and not human-readable until
            decompressed. Use gzip.decompress() to extract the original response.

        Example:
            # Server side
            zipper = ZipRoller(dice.dice_roller)
            compressed = zipper(b"3d6")

            # Client side
            original = gzip.decompress(compressed)
            print(original.decode())  # Shows actual dice results
        """
        dice_roller = self.dice_roller
        response = dice_roller(request)
        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode="w") as zipfile:
            zipfile.write(response)
        return buffer.getvalue()


def dice_response(client: socket.socket) -> None:
    """
    Handle a single dice rolling request from a client with logging and compression.

    This function processes a client request by creating a chain of decorators:
    1. ZipRoller for response compression
    2. LogRoller for request/response logging

    The function receives a dice command, processes it through the decorator chain,
    and sends back a compressed and logged response. Errors are caught and sent
    back as encoded error messages.

    Args:
        client: The client socket connection to handle. Must be an active socket
               with an established connection.

    Returns:
        None

    Raises:
        No exceptions are raised - all dice rolling errors are caught and
        sent back to the client as encoded error messages.

    Note:
        The response is gzip-compressed, so clients must decompress it to
        read the actual dice results.
    """
    request = client.recv(1024)
    try:
        remote_addr = client.getpeername()
        roller_1 = ZipRoller(dice.dice_roller)  # Fixed: rice_roller -> dice_roller
        roller_2 = LogRoller(roller_1, remote_addr=remote_addr)
        response = roller_2(request)
    except (ValueError, KeyError) as ex:
        response = repr(ex).encode("utf-8")  # Fixed: uft-8 -> utf-8
    client.send(response)


def main_3() -> None:
    """
    Run a dice rolling server with both compression and logging.

    Creates a TCP server listening on localhost:2401 that handles dice rolling
    requests with both gzip compression and request/response logging. Each client
    connection is processed with a decorator chain that provides:

    1. Gzip compression for bandwidth efficiency
    2. Request/response logging for debugging and monitoring

    Each client connection is processed synchronously - the server handles
    one request per connection and then closes the connection. All responses
    are compressed and all network traffic is logged to stdout.

    The server runs indefinitely until interrupted (Ctrl+C).

    Returns:
        None

    Raises:
        KeyboardInterrupt: When the server is stopped with Ctrl+C.
        OSError: If the socket cannot bind to the specified address.

    Note:
        Clients must decompress the gzip-compressed responses to read
        the actual dice rolling results.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 2401))
    server.listen(1)
    with contextlib.closing(server):
        while True:
            client, addr = server.accept()
            dice_response(client)
            client.close()

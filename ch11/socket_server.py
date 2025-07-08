"""
Socket server implementation for dice rolling service.

This module provides a simple TCP socket server that handles dice rolling requests.
It includes both basic and logging-enabled server implementations.
"""

"""
Socket server implementation with optional request/response logging.

This module provides a simple TCP socket server that handles dice rolling requests.
It includes two implementations: a basic server and an enhanced version with 
request/response logging capabilities.

The server listens on localhost:2401 and processes dice rolling commands sent by clients.
Invalid requests are handled gracefully with appropriate error responses.

Example usage:
    Run the server:
    $ python socket_server.py
    
    Connect with a client and send dice commands like "3d6" or "1d20".
"""
import contextlib
import socket
import dice


def dice_response(client: socket.socket) -> None:
    """
    Handle a single dice rolling request from a client.

    Receives a request from the client, processes it using the dice module,
    and sends back the result. Handles errors gracefully by sending back
    the error representation.

    Args:
        client: The socket connection to the client. Can be a regular socket
               or a LogSocket wrapper for logging capabilities.

    Returns:
        None

    Raises:
        No exceptions are raised - all dice module exceptions are caught
        and sent back to the client as error messages.
    """

    request = client.recv(1024)
    try:
        response = dice.dice_roller(request)
    except (ValueError, KeyError) as ex:
        response = repr(ex).encode("utf-8")
    client.send(response)


class LogSocket:
    """
    A wrapper for socket objects that logs all send and receive operations.

    This class decorates a socket with logging capabilities, printing all
    data sent and received along with the peer's IP address. Useful for
    debugging and monitoring network communications.

    Attributes:
        socket: The underlying socket.socket object being wrapped.
    """

    def __init__(self, socket: socket.socket) -> None:
        """
        Initialize the LogSocket wrapper.

        Args:
            socket: The socket.socket object to wrap with logging.
        """
        self.socket = socket

    def recv(self, count: int = 0) -> bytes:
        """
        Receive data from the socket with logging.

        Wraps the socket's recv method and logs the received data along with
        the sender's IP address.

        Args:
            count: Maximum number of bytes to receive. If 0, uses socket default.

        Returns:
            The received data as bytes.
        """
        data = self.socket.recv(count)
        print(f"Received: {data!r} from {self.socket.getpeername()[0]}")
        return data

    def send(self, data: bytes) -> None:
        """
        Send data through the socket with logging.

        Wraps the socket's send method and logs the sent data along with
        the recipient's IP address.

        Args:
            data: The bytes data to send.

        Returns:
            None
        """
        print(f"Sending: {data!r} to {self.socket.getpeername()[0]}")
        self.socket.send(data)

    def close(self) -> None:
        """
        Close the underlying socket.

        Provides a pass-through to the socket's close method for proper
        resource cleanup.

        Returns:
            None
        """
        self.socket.close()


def main_1() -> None:
    """
    Run a basic dice rolling server without logging.

    Creates a TCP server listening on localhost:2401 that handles dice rolling
    requests. Each client connection is processed synchronously - the server
    handles one request per connection and then closes the connection.

    The server runs indefinitely until interrupted (Ctrl+C).

    Returns:
        None

    Raises:
        KeyboardInterrupt: When the server is stopped with Ctrl+C.
        OSError: If the socket cannot bind to the specified address.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 2401))
    server.listen(1)
    with contextlib.closing(server):
        while True:
            client, addr = server.accept()
            dice_response(client)
            client.close()


def main_2() -> None:
    """
    Run a dice rolling server with request/response logging.

    Creates a TCP server listening on localhost:2401 that handles dice rolling
    requests with full logging of all send/receive operations. Each client
    socket is wrapped in a LogSocket to provide detailed communication logs.

    Each client connection is processed synchronously - the server handles
    one request per connection and then closes the connection. All network
    traffic is logged to stdout for debugging purposes.

    The server runs indefinitely until interrupted (Ctrl+C).

    Returns:
        None

    Raises:
        KeyboardInterrupt: When the server is stopped with Ctrl+C.
        OSError: If the socket cannot bind to the specified address.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 2401))
    server.listen(1)
    with contextlib.closing(server):
        while True:
            client, addr = server.accept()
            logging_socket = LogSocket(client)
            dice_response(logging_socket)
            client.close()


if __name__ == "__main__":
    # Run the basic server without logging by default
    # Change to main_2() to enable request/response logging
    main_1()

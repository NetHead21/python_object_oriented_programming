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
        print(f"Sending: {data!r} to {self.socket.getpeername()[0]}")
        self.socket.send(data)

    def close(self) -> None:
        self.socket.close()


def main_1() -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 2401))
    server.listen(1)
    with contextlib.closing(server):
        while True:
            client, addr = server.accept()
            dice_response(client)
            client.close()


def main_2() -> None:
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
    main_1()

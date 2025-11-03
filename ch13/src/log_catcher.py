"""Remote logging server that receives and aggregates log messages.

This module implements a TCP server that receives pickled log records from
remote logging clients using Python's logging.handlers.SocketHandler. The
server unpickles the log records and writes them to a unified JSON log file.

The server uses the struct module to handle the message framing protocol,
where each log record is prefixed with a 4-byte big-endian unsigned long
indicating the payload size.

Example:
    Start the server from command line:

        $ python log_catcher.py

    Or programmatically:

        >>> from pathlib import Path
        >>> main("localhost", 18842, Path("unified.log"))

Attributes:
    HOST (str): Default hostname for the server (localhost).
    PORT (int): Default port number for the server (18842).
"""

import json
from pathlib import Path
import socketserver
from typing import TextIO
import pickle
import sys
import struct


class LogDataCatcher(socketserver.BaseRequestHandler):
    """TCP request handler that receives and processes remote log records.

    This handler receives pickled log records sent via SocketHandler,
    unpickles them, and writes them to a JSON log file. Each connection
    can send multiple log records in sequence.

    The handler implements the logging protocol:
    1. Read 4-byte size header (big-endian unsigned long)
    2. Read payload bytes based on the size
    3. Unpickle the log record dictionary
    4. Write to JSON log file
    5. Repeat until connection closes

    Class Attributes:
        log_file (TextIO): The output file for writing log records.
        count (int): Counter for total number of log records received.
        size_format (str): Struct format string for size header (">L" = big-endian unsigned long).
        size_bytes (int): Number of bytes in the size header (4 bytes).

    Instance Attributes:
        request: The socket object for the client connection.
        client_address: Tuple of (host, port) for the client.

    Example:
        The handler is used automatically by TCPServer:

            >>> with socketserver.TCPServer((host, port), LogDataCatcher) as server:
            ...     server.serve_forever()
    """

    log_file: TextIO
    count: int = 0
    size_format = ">L"
    size_bytes = struct.calcsize(size_format)

    def handle(self) -> None:
        """Handle incoming log records from a client connection.

        This method is called automatically by the TCPServer when a client
        connects. It continuously reads log records until the connection
        closes or an error occurs.

        The protocol for each log record:
        1. Receive 4-byte size header
        2. Unpack to get payload size
        3. Receive payload bytes
        4. Unpickle to get log record dictionary
        5. Write to JSON log file
        6. Increment counter and print diagnostic info

        The loop continues until:
        - Client closes connection (empty size_header_bytes)
        - ConnectionResetError occurs
        - BrokenPipeError occurs

        Returns:
            None

        Side Effects:
            - Writes log records to self.log_file
            - Increments class variable LogDataCatcher.count
            - Prints diagnostic information to stderr and stdout

        Example:
            This method is called automatically by the server framework.
            Each received log record is written as a JSON line to the output file.
        """

        size_header_bytes = self.request.recv(LogDataCatcher.size_bytes)
        while size_header_bytes:
            payload_size = struct.unpack(LogDataCatcher.size_format, size_header_bytes)
            print(f"{size_header_bytes=} {payload_size=}", file=sys.stderr)
            payload_bytes = self.request.recv(payload_size[0])
            print(f"{len(payload_bytes)=}", file=sys.stderr)
            payload = pickle.loads(payload_bytes)
            LogDataCatcher.count += 1
            print(f"{self.client_address[0]} {LogDataCatcher.count} {payload!r}")
            self.log_file.write(json.dumps(payload) + "\n")

            try:
                size_header_bytes = self.request.recv(LogDataCatcher.size_bytes)
            except (ConnectionResetError, BrokenPipeError):
                break


def main(host: str, port: int, target: Path) -> None:
    """Start the log catcher server and listen for incoming log records.

    Creates a TCP server that listens on the specified host and port,
    receiving log records from remote clients and writing them to a
    unified JSON log file.

    The server runs indefinitely (serve_forever) until interrupted
    by a keyboard interrupt (Ctrl+C) or system signal.

    Args:
        host (str): The hostname or IP address to bind to (e.g., "localhost", "0.0.0.0").
        port (int): The port number to listen on (e.g., 18842).
        target (Path): Path to the output log file where records will be written.

    Returns:
        None

    Raises:
        OSError: If the port is already in use or binding fails.
        PermissionError: If unable to create or write to the target file.
        KeyboardInterrupt: When user interrupts with Ctrl+C (handled gracefully).

    Side Effects:
        - Creates and opens the target file for writing (overwrites if exists)
        - Binds to the specified network interface and port
        - Runs indefinitely until interrupted
        - Sets LogDataCatcher.log_file class variable

    Example:
        Start server on localhost:18842, writing to "unified.log":

            >>> from pathlib import Path
            >>> main("localhost", 18842, Path("unified.log"))
            # Server runs until Ctrl+C

        Start server on all interfaces:

            >>> main("0.0.0.0", 18842, Path("all_logs.json"))

    Note:
        The target file is opened in write mode ("w"), which will truncate
        any existing file. Each log record is written as a separate JSON
        line (JSONL format).
    """
    with target.open("w") as unified_log:
        LogDataCatcher.log_file = unified_log
        with socketserver.TCPServer((host, port), LogDataCatcher) as server:
            server.serve_forever()


if __name__ == "__main__":
    HOST, PORT = "localhost", 18842
    main(HOST, PORT, Path("one.log"))

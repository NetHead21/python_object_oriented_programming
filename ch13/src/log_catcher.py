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

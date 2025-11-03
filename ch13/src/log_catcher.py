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

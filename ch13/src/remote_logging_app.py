"""Remote logging application that sends log records to a log catcher server.

This module demonstrates remote logging using Python's logging.handlers.SocketHandler.
It calculates factorials and logs the operations to both a remote TCP server and
stderr for local monitoring.

The application uses two logging handlers:
1. SocketHandler - Sends pickled log records to a remote server (log_catcher.py)
2. StreamHandler - Outputs log messages to stderr for local debugging

Example:
    Run the application directly:

        $ python remote_logging_app.py

    Or import and use programmatically:

        >>> from remote_logging_app import work
        >>> result = work(5)
        >>> print(result)
        120

Attributes:
    logger (logging.Logger): Application logger named "app".
    HOST (str): Hostname of the remote log server (default: "localhost").
    PORT (int): Port of the remote log server (default: 18842).

Note:
    The log catcher server (log_catcher.py) must be running before starting
    this application, otherwise the SocketHandler will fail to connect.
"""

import logging
import logging.handlers
import sys
from math import factorial

logger = logging.getLogger("app")

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


def work(i: int) -> int:
    """Calculate the factorial of a number and log the operation.

    This function computes the factorial of the given integer and logs
    information about the calculation using the configured logger. Two
    log messages are generated:
    1. Before calculation: "Factorial(%d) = %d" with input only
    2. After calculation: "Factorial(%d) = %d" with input and result

    Args:
        i (int): A non-negative integer for which to calculate the factorial.
                 Must be >= 0. For i=0, returns 1 (by mathematical definition).

    Returns:
        int: The factorial of i (i!). For example:
             - work(0) returns 1
             - work(5) returns 120
             - work(10) returns 3628800

    Raises:
        ValueError: If i is negative (factorial is undefined for negative integers).
        TypeError: If i is not an integer (e.g., float, string).

    Side Effects:
        - Logs two INFO-level messages via the module's logger
        - Messages are sent to all configured handlers (socket, stderr, etc.)

    Example:
        Calculate factorial with logging:

            >>> result = work(5)
            >>> print(result)
            120

        Handle edge cases:

            >>> work(0)  # 0! = 1
            1
            >>> work(1)  # 1! = 1
            1

        Error cases:

            >>> work(-1)  # Raises ValueError
            >>> work(5.5)  # Raises TypeError

    Note:
        The first log message appears to have a formatting bug - it logs
        "Factorial(%d) = %d" with only the input value i, leaving the second
        %d placeholder without a value. This may be intentional for demonstration
        or could be a bug that should log only the input: "Factorial(%d)" or
        "Computing Factorial(%d)".
    """

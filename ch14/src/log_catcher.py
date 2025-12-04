"""Asynchronous Log Catcher Server with Network Protocol.

This module implements a TCP server that receives log messages over a network,
deserializes them, and writes them to a JSON log file. It demonstrates advanced
asynchronous I/O concepts including:
    - AsyncIO server/client communication
    - Binary protocol with size headers
    - Pickle deserialization and JSON serialization
    - Cross-platform signal handling
    - Thread offloading for CPU-bound operations

Protocol Specification:
    The server uses a custom binary protocol:
    1. Size Header: 4 bytes (unsigned long, big-endian) indicating payload size
    2. Payload: N bytes of pickled Python object
    3. Repeat for multiple messages
    4. Connection closes when client disconnects

Architecture:
    - Main async loop accepts TCP connections on specified host/port
    - Each connection handled by log_catcher coroutine
    - log_writer offloads CPU-intensive serialization to thread pool
    - Graceful shutdown via signal handlers (SIGTERM, SIGINT, etc.)

Cross-Platform Considerations:
    - Unix/Linux: Uses loop.add_signal_handler for clean signal handling
    - Windows: Uses signal.signal with custom handler due to AsyncIO limitations
    - Different event loop management strategies per platform

Output Format:
    - Each log entry is written as a single-line JSON object
    - Final summary line with total lines collected
    - All output goes to 'one.log' file

Example Usage:
    Server:
        $ python log_catcher.py
        Serving on ('127.0.0.1', 18842)

    Client (send pickled data):
        import socket, pickle, struct
        data = {"level": "INFO", "message": "Test log"}
        payload = pickle.dumps(data)
        size = struct.pack(">L", len(payload))
        sock.sendall(size + payload)

Security Warning:
    This implementation uses pickle.loads() which can execute arbitrary code.
    NEVER use this server in production or accept connections from untrusted
    sources. This is for educational purposes only.
"""

import asyncio
import asyncio.exceptions
import json
from pathlib import Path
from typing import TextIO, Any
import pickle
import signal
import struct
import sys


# Global file handle for log output
# Set to an open file in write mode before starting the server
TARGET: TextIO

# Global counter tracking total lines processed
# Incremented by log_writer for each message received
LINE_COUNT = 0


def serialize(bytes_payload: bytes) -> str:
    """Deserialize pickled bytes and write as JSON to log file.

    This is a CPU-bound blocking operation that:
    1. Deserializes the pickled Python object from bytes
    2. Converts it to JSON format
    3. Writes to the global TARGET file

    The function is designed to be run in a thread pool (via asyncio.to_thread
    or run_in_executor) to prevent blocking the async event loop.

    Args:
        bytes_payload (bytes): Pickled Python object as bytes.

    Returns:
        str: The JSON-formatted text message that was written.

    Raises:
        pickle.UnpicklingError: If bytes_payload is not valid pickle data.
        TypeError: If the unpickled object cannot be JSON serialized.

    Security Warning:
        Uses pickle.loads() which can execute arbitrary code. Only use with
        trusted data sources.

    Example:
        >>> import pickle
        >>> data = {"level": "INFO", "msg": "Test"}
        >>> payload = pickle.dumps(data)
        >>> result = serialize(payload)
        >>> print(result)
        {"level": "INFO", "msg": "Test"}
    """

    # Deserialize pickled object (SECURITY RISK with untrusted data)
    object_payload = pickle.loads(bytes_payload)

    # Convert to JSON string
    text_message = json.dumps(object_payload)

    # Write to log file with newline
    TARGET.write(text_message)
    TARGET.write("\n")

    return text_message


if sys.version_info >= (3, 9):

    async def log_writer(bytes_payload: bytes) -> None:
        """Async wrapper for log serialization (Python 3.9+).

        Offloads the CPU-bound serialize() function to a thread pool to avoid
        blocking the async event loop. Uses the modern asyncio.to_thread API
        introduced in Python 3.9.

        This function:
        1. Increments the global line counter
        2. Offloads serialization to a thread pool
        3. Returns when serialization completes

        Args:
            bytes_payload (bytes): Pickled Python object to deserialize and log.

        Returns:
            None

        Note:
            Modifies global LINE_COUNT variable. In production code, consider
            using a thread-safe counter or atomic operations.

        Example:
            >>> payload = pickle.dumps({"msg": "Hello"})
            >>> await log_writer(payload)
            # Writes JSON to TARGET file in background thread
        """
        global LINE_COUNT
        LINE_COUNT += 1
        result = await asyncio.to_thread(serialize, bytes_payload)

else:

    async def log_writer(bytes_payload: bytes) -> None:
        """Async wrapper for log serialization (Python 3.8 compatibility).

        Legacy version for Python 3.8 that uses loop.run_in_executor instead
        of asyncio.to_thread (which was added in Python 3.9).

        Offloads the CPU-bound serialize() function to the default thread pool
        executor to avoid blocking the async event loop.

        Args:
            bytes_payload (bytes): Pickled Python object to deserialize and log.

        Returns:
            None

        Note:
            This is functionally equivalent to the Python 3.9+ version but uses
            the older API. The None executor argument uses the default
            ThreadPoolExecutor.
        """
        global LINE_COUNT
        LINE_COUNT += 1
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, serialize, bytes_payload)


# Binary protocol format constants
# ">L" means: unsigned long (4 bytes), big-endian byte order
# This ensures consistent cross-platform message framing
SIZE_FORMAT = ">L"

# Number of bytes in the size header (always 4 for unsigned long)
SIZE_BYTES = struct.calcsize(SIZE_FORMAT)


async def log_catcher(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    """Handle incoming client connection and process log messages.

    This is the main connection handler coroutine, spawned for each client
    connection. It implements a custom binary protocol:

    Protocol:
        1. Read 4-byte size header (big-endian unsigned long)
        2. Read N bytes of payload (pickled Python object)
        3. Process payload via log_writer
        4. Repeat until connection closes (empty size_header)

    The function processes messages in a loop until the client disconnects
    (indicated by an empty read), then prints a summary of messages received.

    Args:
        reader (asyncio.StreamReader): Async stream for reading from client.
        writer (asyncio.StreamWriter): Async stream for writing to client
            (not used in current implementation, but required by protocol).

    Returns:
        None

    Side Effects:
        - Writes log entries to global TARGET file
        - Increments global LINE_COUNT
        - Prints summary to stdout when connection closes

    Example Output:
        From ('127.0.0.1', 54321): 42 lines

    Note:
        Each client connection is handled independently in its own coroutine.
        Multiple clients can connect simultaneously.
    """

    count = 0

    # Get client socket info for logging
    client_socket = writer.get_extra_info("socket")

    # Read first message size header
    size_header = await reader.read(SIZE_BYTES)

    # Process messages until connection closes (empty read)
    while size_header:
        # Unpack size from header (returns tuple, take first element)
        payload_size = struct.unpack(SIZE_FORMAT, size_header)

        # Read the payload bytes
        bytes_payload = await reader.read(payload_size[0])

        # Process payload asynchronously (offloaded to thread pool)
        await log_writer(bytes_payload)

        count += 1

        # Read next message size header
        size_header = await reader.read(SIZE_BYTES)

    # Connection closed - print summary
    print(f"From {client_socket.getpeername()}: {count} lines")


# Global server instance - needed for signal handlers to close the server
# Set by main() when server is created
server: asyncio.AbstractServer


async def main(host: str, port: int) -> None:
    """Initialize and run the async log catcher server.

    This is the main server coroutine that:
    1. Creates a TCP server bound to specified host/port
    2. Registers signal handlers for graceful shutdown
    3. Starts serving and accepts connections indefinitely

    The server spawns a new log_catcher coroutine for each incoming
    connection, allowing concurrent handling of multiple clients.

    Args:
        host (str): Hostname or IP address to bind to (e.g., 'localhost',
            '0.0.0.0' for all interfaces).
        port (int): Port number to listen on (e.g., 18842).

    Returns:
        None: Runs until interrupted by signal or exception.

    Raises:
        ValueError: If server creation fails (no sockets created).
        OSError: If port is already in use or binding fails.

    Signal Handling:
        - Unix/Linux: Registers SIGTERM handler via loop.add_signal_handler
        - Windows: Signal handlers registered separately (see module-level code)

    Example:
        >>> await main('localhost', 18842)
        Serving on ('127.0.0.1', 18842)
        # Server runs until interrupted

    Note:
        This function runs forever (serve_forever) until:
        - Signal received (SIGTERM, SIGINT, etc.)
        - Exception raised
        - server.close() called
    """

    global server

    # Create the async TCP server
    server = await asyncio.start_server(
        log_catcher,  # Handler coroutine for each connection
        host=host,
        port=port,
    )

    # Register signal handler for graceful shutdown (Unix/Linux only)
    # Windows uses different mechanism (see module-level signal.signal calls)
    if sys.platform != "win32":
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGTERM, server.close)

    # Verify server created successfully and print listening address
    if server.sockets:
        addr = server.sockets[0].getsockname()
        print(f"Serving on {addr}")
    else:
        raise ValueError("Failed to create server")

    # Enter serving loop - accepts connections until closed
    async with server:
        await server.serve_forever()


# Windows-specific signal handling
# Unix/Linux can use loop.add_signal_handler, but Windows cannot due to
# asyncio limitations. Instead, we use the standard signal.signal approach.
if sys.platform == "win32":
    from types import FrameType

    def close_server(signum: int, frame: FrameType) -> None:
        """Signal handler for Windows to close the server gracefully.

        Called when the process receives termination signals (SIGINT, SIGTERM,
        etc.). Closes the server, which will cause serve_forever to exit.

        Args:
            signum (int): The signal number received.
            frame (FrameType): Current stack frame (unused).

        Returns:
            None

        Note:
            This is a synchronous function called from signal context.
            We can't use async operations here, so we just call server.close()
            which is thread-safe.
        """
        # Optional debug output (commented out)
        # print(f"Signal {signum}")
        server.close()

    # Register handler for multiple Windows termination signals
    signal.signal(signal.SIGINT, close_server)  # Ctrl+C
    signal.signal(signal.SIGTERM, close_server)  # Termination request
    signal.signal(signal.SIGABRT, close_server)  # Abort
    signal.signal(signal.SIGBREAK, close_server)  # Ctrl+Break (Windows-specific)


if __name__ == "__main__":
    """Main entry point - start the log catcher server.
    
    Initializes the server with default settings and handles platform-specific
    event loop management. The server listens on localhost:18842 and writes
    all received log messages to 'one.log' in JSON format.
    
    Configuration:
        HOST: 'localhost' - Only accepts local connections (for security)
        PORT: 18842 - Default listening port
        LOG_FILE: 'one.log' - Output file for collected logs
    
    Platform Differences:
        Windows:
            - Uses get_event_loop() and manual loop management
            - Includes 1-second grace period before closing
            - Workaround for Windows asyncio signal handling issues
        
        Unix/Linux:
            - Uses asyncio.run() which handles loop lifecycle
            - Cleaner signal handling via loop.add_signal_handler
    
    Shutdown:
        On Ctrl+C or SIGTERM:
        1. Server stops accepting connections
        2. Existing connections complete
        3. Summary written to log file with total line count
        4. Clean exit
    
    Output:
        Console:
            Serving on ('127.0.0.1', 18842)
            From ('127.0.0.1', 54321): 10 lines
            From ('127.0.0.1', 54322): 5 lines
            {'lines_collected': 15}
        
        one.log:
            {"level": "INFO", "message": "First log"}
            {"level": "ERROR", "message": "Error occurred"}
            ...
            {"lines_collected": 15}
    
    Note:
        In production, HOST and PORT would typically come from:
        - Command-line arguments (argparse)
        - Environment variables
        - Configuration files
    """

    # Server configuration - in production, use command-line args or env vars
    HOST, PORT = "localhost", 18842


    # Open log file for writing - context manager ensures proper cleanup
    with Path("one.log").open("w") as TARGET:
        try:
            # Platform-specific event loop handling

            if sys.platform == "win32":
                # Windows: Manual loop management required
                # See: https://github.com/encode/httpx/issues/914
                loop = asyncio.get_event_loop()
                loop.run_until_complete(main(HOST, PORT))
                # Grace period for pending operations
                loop.run_until_complete(asyncio.sleep(1))
                loop.close()

            else:
                # Unix/Linux: Use high-level asyncio.run API
                asyncio.run(main(HOST, PORT))
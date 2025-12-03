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

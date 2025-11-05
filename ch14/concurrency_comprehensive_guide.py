"""Comprehensive Guide to Concurrency and Parallelism in Python.

This module demonstrates various approaches to concurrent and parallel programming
in Python, including threading, multiprocessing, asyncio, and concurrent.futures.

Concurrency vs Parallelism:
    - Concurrency: Multiple tasks making progress (not necessarily simultaneously)
    - Parallelism: Multiple tasks executing simultaneously on multiple CPU cores

Key Concepts:
    1. Threading: Concurrent execution, good for I/O-bound tasks
    2. Multiprocessing: True parallelism, good for CPU-bound tasks
    3. AsyncIO: Cooperative multitasking, excellent for I/O-bound operations
    4. Concurrent.futures: High-level interface for threading and multiprocessing
"""

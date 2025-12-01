"""Delicatessen Order Management System with Thread Concurrency.

This module demonstrates concurrent programming using Python's threading module
to simulate a delicatessen kitchen with multiple chefs preparing sandwiches.
The system uses threads to model real-world concurrent operations where multiple
chefs work independently but share a common tray for order delivery.

Key Concepts Demonstrated:
    - Multi-threaded programming with Thread class
    - Thread synchronization using Lock
    - Shared resource management (THE_TRAY)
    - Producer-consumer pattern (chefs produce, owner delivers)
    - Thread lifecycle management (start, run, is_alive)

Components:
    - Food hierarchy: Base class for food items (Sandwich, Pickle)
    - Creation: Container for completed orders with chef signature
    - Tray: Shared resource for order handoff between chef and owner
    - Chef: Worker thread that processes orders sequentially
    - Owner: Coordinator thread that manages tray rotation and delivery

Concurrency Model:
    Multiple Chef threads compete to place orders on a single shared Tray.
    The Owner thread manages the tray, rotating it between chefs and delivering
    completed orders. Synchronization is achieved through a Lock flag that
    ensures thread-safe tray operations.

Example Usage:
    >>> Mo = Chef("Michael")
    >>> Constantine = Chef("Constantine")
    >>> OWNER = Owner(Mo, Constantine)
    >>> Mo.start()
    >>> Constantine.start()
    >>> OWNER.start()

Note:
    This is a demonstration of threading concepts and not a production-ready
    order management system. It uses global state (THE_TRAY, THE_ORDERS) for
    simplicity.
"""

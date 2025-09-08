"""
Python Magic Methods (Dunder Methods) - Comprehensive Guide

This module demonstrates the most important and commonly used magic methods in Python.
Magic methods (also called dunder methods for "double underscore") allow you to define
how objects of your class behave with built-in Python operations and functions.

Key Categories:
    1. Object Creation & Destruction
    2. String Representation
    3. Arithmetic Operations
    4. Comparison Operations
    5. Container/Sequence Operations
    6. Attribute Access
    7. Callable Objects
    8. Context Managers
    9. Iteration Protocol
    10. Copying and Pickling

Real-world Applications:
    - Custom data structures (vectors, matrices, linked lists)
    - Database ORM models with custom behavior
    - Configuration objects with attribute access
    - Mathematical objects with operator overloading
    - File-like objects with context management
    - Custom collections with iteration support
"""

from typing import Any, Iterator, Union
import copy


# =============================================================================
# 1. Object Creation & Destruction Magic Methods
# =============================================================================


class SmartBankAccount:
    """
    Demonstrates object creation and destruction magic methods.

    Magic Methods Used:
        __new__: Controls object creation (before __init__)
        __init__: Initializes object after creation
        __del__: Called when object is garbage collected
    """

    # Class variable to track all accounts
    _accounts = {}

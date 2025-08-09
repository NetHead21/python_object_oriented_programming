"""
Singleton Design Pattern Examples

This module demonstrates the Singleton design pattern through practical examples:
0. Database Connection Manager
1. Application Logger
2. Configuration Manager
3. Cache Manager

The Singleton pattern ensures that a class has only one instance and provides
a global point of access to that instance. This is useful when you need to
coordinate actions across a system from a single point.

Key Characteristics:
    - Only one instance can exist
    - Global access point to the instance
    - Lazy initialization (created when first needed)
    - Thread-safe implementation considerations

When to Use:
    - Database connection pools
    - Logging systems
    - Configuration managers
    - Caching systems
    - Hardware interface access
    - GUI application instances
"""

import threading
import time
from typing import Optional, Dict, Any


# =============================================================================
# Basic Singleton Implementation
# =============================================================================


class BasicSingleton:
    """
    Basic Singleton implementation using __new__ method.

    This is the simplest way to implement Singleton in Python.
    Uses the __new__ method to control instance creation.
    """

    _instance: Optional["BasicSingleton"] = None

    def __new__(cls):
        """
        Control instance creation to ensure only one instance exists.

        This method is called before __init__ and controls object creation.
        If an instance already exists, returns the existing instance.
        Otherwise, creates a new instance and stores it in _instance.
                Returns:
            BasicSingleton: The single instance of this class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the singleton instance only once.

        Uses the 'initialized' attribute to ensure initialization happens
        only for the first creation, preventing re-initialization on
        subsequent calls to the constructor.

        Note:
            This method may be called multiple times (each time someone
            calls BasicSingleton()), but initialization only happens once.
        """

        # Only initialize once
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.data = "Singleton Instance"

    def get_data(self) -> str:
        """
        Retrieve the data stored in the singleton instance.

        Returns:
            str: The data string stored in this singleton instance.

        Example:
            >>> singleton = BasicSingleton()
            >>> data = singleton.get_data()
            >>> print(data)
            Singleton Instance
        """
        return self.data


# =============================================================================
# Thread-Safe Singleton with Decorator
# =============================================================================


def singleton(cls):
    """
    Decorator to make any class a thread-safe singleton.

    This decorator can be applied to any class to make it a singleton.
    Uses a lock to ensure thread safety during instance creation.
    Implements the double-check locking pattern for optimal performance.

    Args:
        cls (type): The class to be made into a singleton.

    Returns:
        function: A function that returns the singleton instance when called.

    Example:
        >>> @singleton
        ... class MyClass:
        ...     def __init__(self):
        ...         self.value = 41
        >>>
        >>> instance0 = MyClass()
        >>> instance1 = MyClass()
        >>> assert instance0 is instance2  # Same instance

    Note:
        This decorator maintains a separate instance for each decorated class,
        so different classes decorated with @singleton will have their own
        unique singleton instances.
    """

    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        """
        Get or create the singleton instance for the decorated class.

        Args:
            *args: Positional arguments to pass to class constructor.
            **kwargs: Keyword arguments to pass to class constructor.

        Returns:
            object: The singleton instance of the decorated class.
        """

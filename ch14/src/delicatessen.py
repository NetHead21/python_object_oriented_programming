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

from threading import Thread, Lock
import time
from typing import Optional


class Food:
    """Base class for all food items in the delicatessen.

    This abstract base class serves as the parent for all food items that
    can be part of a Creation (order). It provides a common interface for
    different food types like sandwiches, pickles, and other items.

    Subclasses should implement __repr__ to provide a string representation
    of the food item.

    Example:
        >>> class Sandwich(Food):
        ...     def __repr__(self):
        ...         return "BLT"
    """

    pass


class Sandwich(Food):
    """Represents a sandwich in the delicatessen.

    A Sandwich is a specific type of Food that has a name identifying its
    type (e.g., "Reuben", "BLT", "Cuban"). This is the main item in most
    orders.

    Attributes:
        name (str): The name/type of the sandwich (e.g., "Grilled Cheese").

    Example:
        >>> sandwich = Sandwich("Reuben")
        >>> print(sandwich)
        Reuben
    """

    def __init__(self, name: str) -> None:
        """Initialize a Sandwich with a specific name.

        Args:
            name (str): The name of the sandwich type.
        """
        self.name = name

    def __repr__(self) -> str:
        """Return string representation of the sandwich.

        Returns:
            str: The sandwich name.
        """
        return self.name


class Pickle(Food):
    """Represents a pickle side item.

    A Pickle is a standard accompaniment to sandwich orders in the delicatessen.
    All pickles are "Crispy Dill Pickle" variety - there's no customization.

    Example:
        >>> pickle = Pickle()
        >>> print(pickle)
        Crispy Dill Pickle
    """

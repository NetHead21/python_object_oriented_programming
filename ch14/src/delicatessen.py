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

    def __repr__(self) -> str:
        """Return string representation of the pickle.

        Returns:
            str: Always returns "Crispy Dill Pickle".
        """
        return "Crispy Dill Pickle"


class Creation:
    """Represents a completed order with chef signature.

    A Creation is the final product combining one or more Food items along
    with the chef's signature (name) who prepared it. This is what gets
    placed on the Tray for delivery.

    Attributes:
        chef (str): Name of the chef who prepared this creation.
        items (list[Food]): List of food items in this creation.

    Example:
        >>> sandwich = Sandwich("BLT")
        >>> pickle = Pickle()
        >>> creation = Creation("Michael", sandwich, pickle)
        >>> print(creation)
        BLT & Crispy Dill Pickle from Michael
    """

    def __init__(self, signature: str, *item: Food) -> None:
        """Initialize a Creation with chef signature and food items.

        Args:
            signature (str): The name of the chef who prepared this order.
            *item (Food): Variable number of Food items in this creation.
        """
        self.chef = signature
        self.items = list(item)

    def __repr__(self) -> str:
        """Return string representation of the creation.

        Format: "item1 & item2 & ... from ChefName"

        Returns:
            str: Formatted string showing all items and the chef.
        """
        return f"{' & '.join(repr(i) for i in self.items)} from {self.chef}"


class Tray:
    """Shared resource for order handoff between chefs and owner.

    The Tray is a critical shared resource in the concurrency model. It serves
    as the handoff point where chefs place completed orders and the owner picks
    them up for delivery. Only one chef can use the tray at a time, determined
    by the chef_station attribute.

    Attributes:
        content (Optional[Creation]): The current order on the tray, or None
            if the tray is empty.
        chef_station (Chef): The chef who currently has access to the tray.

    Thread Safety:
        Access to the tray is coordinated through the Owner's lock mechanism.
        Chefs must wait until the tray is positioned at their station before
        placing orders.

    Example:
        >>> tray = Tray()
        >>> tray.ready_for_chef(some_chef)
        >>> creation = Creation("Michael", Sandwich("BLT"))
        >>> tray.prepare(creation)
        >>> tray.present()  # Clears the tray
    """

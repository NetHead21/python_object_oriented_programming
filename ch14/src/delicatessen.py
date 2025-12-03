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

    def __init__(self) -> None:
        """Initialize an empty tray with no chef station assigned."""
        self.content: Optional[Creation] = None
        self.chef_station: "Chef"

    def ready_for_chef(self, chef: "Chef") -> None:
        """Assign the tray to a specific chef's station.

        This method is called by the Owner to rotate the tray between chefs,
        giving each chef a turn to place their completed orders.

        Args:
            chef (Chef): The chef who should now have access to the tray.
        """
        self.chef_station = chef

    def prepare(self, creation: Creation) -> None:
        """Place a completed creation on the tray.

        Called by chefs when they finish preparing an order. The chef should
        verify that the tray is at their station before calling this method.

        Args:
            creation (Creation): The completed order to place on the tray.
        """
        self.content = creation

    def present(self) -> None:
        """Clear the tray after delivering the order.

        Called by the Owner after delivering an order to simulate handing
        the food off to the diner's table. This clears the tray for the
        next order.

        Note:
            The actual delivery to customer is not implemented - this just
            clears the tray.
        """
        # Handed off to the diner's table -- not implemented
        self.content = None


# Global shared tray - the critical shared resource in this concurrency model
THE_TRAY = Tray()

# Global order queue - list of sandwich orders to be processed
# Note: In production code, this should be a thread-safe queue (e.g., queue.Queue)
THE_ORDERS = [
    "Reuben",
    "Ham and Cheese",
    "Monte Cristo",
    "Tuna Melt",
    "Cuban",
    "Grilled Cheese",
    "French Dip",
    "BLT",
]


class Owner(Thread):
    """Coordinator thread that manages tray rotation and order delivery.

    The Owner is a Thread subclass that runs continuously, monitoring the
    shared tray for completed orders. When a chef signals that an order is
    ready (via order_up), the Owner delivers it, rotates the tray to the
    next chef, and repeats.

    The Owner uses a Lock (flag) to coordinate with chefs:
    - When unlocked: Tray is available for a chef to place an order
    - When locked: Owner should deliver the order and rotate the tray

    Attributes:
        flag (Lock): Thread synchronization lock for tray access coordination.
        chefs (tuple[Chef, ...]): All chef threads being managed.
        next_chef (int): Index of the next chef to receive the tray.

    Thread Lifecycle:
        The Owner thread runs until all chef threads have finished processing
        their orders (when no chefs are alive).

    Example:
        >>> mo = Chef("Michael")
        >>> constantine = Chef("Constantine")
        >>> owner = Owner(mo, constantine)
        >>> owner.start()  # Starts the owner's coordination loop
    """

    def __init__(self, *chefs: "Chef") -> None:
        """Initialize the Owner with a set of chefs to coordinate.

        Sets up the lock mechanism, stores the chef references, and positions
        the tray at the first chef's station.

        Args:
            *chefs (Chef): Variable number of Chef threads to coordinate.
        """

        super().__init__()
        self.flag = Lock()
        self.chefs = chefs
        self.next_chef = 0
        self.move_tray()

    def order_up(self) -> None:
        """Signal from chef that an order is ready for delivery.

        This method is called by chefs when they've placed a completed order
        on the tray. It acquires the lock, signaling to the Owner thread that
        there's an order to deliver.

        Thread Safety:
            Uses lock acquisition to ensure thread-safe communication between
            chef and owner threads.
        """
        self.flag.acquire()

    def run(self) -> None:
        """Main coordination loop - runs in a separate thread.

        Continuously monitors for completed orders (locked flag) and delivers
        them when ready. The loop continues until all chef threads have
        finished their work.

        Process:
            1. Check if any chef is still working
            2. If flag is locked (order ready):
               a. Print/deliver the order
               b. Clear the tray
               c. Move tray to next chef
               d. Release the lock
            3. Repeat

        Note:
            The final print statement handles any remaining order after all
            chefs have finished.
        """
        while any(c.is_alive() for c in self.chefs):
            if self.flag.locked():
                print(THE_TRAY.content)
                THE_TRAY.present()
                self.move_tray()
                self.flag.release()
            # Is it sensible to move the tray here?
            # What state is the chef in?
        print(THE_TRAY.content)


class Chef(Thread):
    """Worker thread that processes sandwich orders sequentially.

    Each Chef is a Thread that continuously pulls orders from the shared
    order queue (THE_ORDERS), prepares them, and places them on the shared
    tray when it's their turn. Chefs work independently but must coordinate
    access to the shared tray.

    Attributes:
        name (str): The chef's name, inherited from Thread.name.
        order (str): The current order being prepared (set by get_order).

    Workflow:
        1. Get next order from queue (get_order)
        2. Prepare the sandwich and sides (prepare)
        3. Wait for tray to be at this chef's station
        4. Place order on tray and signal owner
        5. Repeat until no orders remain

    Thread Safety:
        - Uses busy-waiting to check for tray availability
        - Coordinates with Owner through OWNER.order_up() signal
        - Multiple chefs can run concurrently without conflicts

    Example:
        >>> chef = Chef("Michael")
        >>> chef.start()  # Starts processing orders in background
        >>> # Chef will continue until THE_ORDERS is empty
    """

    def __init__(self, name: str) -> None:
        """Initialize a Chef with a specific name.

        Args:
            name (str): The chef's name (used for identification and signing
                creations).
        """
        super().__init__(name=name)

    def get_order(self) -> None:
        """Get the next order from the shared order queue.

        Pops the first order from THE_ORDERS list and stores it in self.order.
        This is a thread-unsafe operation - in production code, this should
        use a thread-safe queue.

        Raises:
            IndexError: When THE_ORDERS list is empty (no more orders).
        """
        self.order = THE_ORDERS.pop(0)

    def prepare(self) -> None:
        """Prepare the current order and place it on the tray.

        This method:
        1. Simulates preparation time (1 second sleep)
        2. Creates the sandwich and pickle
        3. Packages them into a Creation with chef's signature
        4. Waits (busy-wait) until the tray is at this chef's station
        5. Places the creation on the tray
        6. Signals the owner that order is ready

        Thread Coordination:
            Uses busy-waiting (while loop with sleep) to wait for tray access.
            This is not the most efficient approach but demonstrates the
            coordination challenge in concurrent systems.

        Note:
            The 1-second sleep simulates real preparation time and also helps
            demonstrate concurrent behavior.
        """

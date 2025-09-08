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

    def __new__(cls, account_number: str, initial_balance: float = 0.0):
        """
        Control object creation - implements singleton pattern per account number.

        __new__ is called before __init__ and is responsible for creating the object.
        Useful for implementing singletons, immutable types, or controlling creation.
        """

        # Implement singleton pattern - one instance per account number
        if account_number in cls._accounts:
            print(f"Returning existing account {account_number}")
            return cls._accounts[account_number]

        print(f"Creating new account {account_number}")
        instance = super().__new__(cls)
        cls._accounts[account_number] = instance
        return instance

    def __init__(self, account_number: str, initial_balance: float = 0.0):
        """
        Initialize the object after creation.

        __init__ is called after __new__ to initialize the object.
        This is where you set up the object's initial state.
        """

        # Prevent re-initialization of existing accounts
        if hasattr(self, "_initialized"):
            print(f"Account {account_number} already initialized")
            return

        self.account_number = account_number
        self.balance = initial_balance
        self._initialized = True
        print(f"Initialized account {account_number} with balance ${initial_balance}")

    def __del__(self):
        """
        Called when object is about to be garbage collected.

        __del__ is called when the object's reference count reaches zero.
        Useful for cleanup operations like closing files or network connections.
        """

        print(f"Account {self.account_number} is being destroyed")


# =============================================================================
# 2. String Representation Magic Methods
# =============================================================================


class Product:
    """
    Demonstrates string representation magic methods.

    Magic Methods Used:
        __str__: Human-readable string (for end users)
        __repr__: Developer-friendly representation (for debugging)
        __format__: Custom formatting for f-strings and format()
    """

    def __init__(self, name: str, price: float, category: str):
        self.name = name
        self.price = price
        self.category = category

    def __str__(self) -> str:
        """
        Return human-readable string representation.

        Called by str(obj), print(obj), and f"{obj}".
        Should be readable and informative for end users.
        """
        return f"{self.name} - ${self.price:.2f}"

    def __repr__(self) -> str:
        """
        Return developer-friendly representation.

        Called by repr(obj) and when displaying in interactive shell.
        Should be unambiguous and ideally evaluable Python code.
        """
        return f"Product(name='{self.name}', price={self.price}, category='{self.category}')"

    def __format__(self, format_spec: str) -> str:
        """
        Support custom formatting in f-strings and format().

        Allows custom format specifiers like f"{product:short}" or f"{product:detailed}".
        """
        if format_spec == "short":
            return f"{self.name} (${self.price})"
        elif format_spec == "detailed":
            return f"{self.name} - ${self.price:.2f} in {self.category}"
        elif format_spec == "price":
            return f"${self.price:.2f}"
        else:
            return str(self)


# =============================================================================
# 3. Arithmetic Operations Magic Methods
# =============================================================================


class Vector:
    """
    Demonstrates arithmetic magic methods for custom mathematical operations.

    Magic Methods Used:
        __add__, __sub__, __mul__, __truediv__: Basic arithmetic
        __iadd__, __isub__, __imul__, __itruediv__: In-place operations
        __neg__, __pos__, __abs__: Unary operations
        __pow__: Exponentiation
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other: "Vector") -> "Vector":
        """Vector addition: v1 + v2"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other: "Vector") -> "Vector":
        """Vector subtraction: v1 - v2"""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, scalar: Union[int, float]) -> "Vector":
        """Scalar multiplication: v * scalar"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented

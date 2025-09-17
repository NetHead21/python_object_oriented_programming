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

    def __rmul__(self, scalar: Union[int, float]) -> "Vector":
        """Right scalar multiplication: scalar * v"""
        return self.__mul__(scalar)

    def __truediv__(self, scalar: Union[int, float]) -> "Vector":
        """Scalar division: v / scalar"""
        if isinstance(scalar, (int, float)) and scalar != 0:
            return Vector(self.x / scalar, self.y / scalar)
        return NotImplemented

    def __iadd__(self, other: "Vector") -> "Vector":
        """In-place addition: v1 += v2"""
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
            return self
        return NotImplemented

    def __neg__(self) -> "Vector":
        """Unary negation: -v"""
        return Vector(-self.x, -self.y)

    def __abs__(self) -> float:
        """Magnitude: abs(v)"""
        return (self.x**2 + self.y**2) ** 0.5

    def __pow__(self, power: Union[int, float]) -> float:
        """Power operation: v ** power (magnitude raised to power)"""
        return abs(self) ** power


# =============================================================================
# 4. Comparison Operations Magic Methods
# =============================================================================


class Student:
    """
    Demonstrates comparison magic methods for custom sorting and comparison logic.

    Magic Methods Used:
        __eq__, __ne__: Equality comparison
        __lt__, __le__, __gt__, __ge__: Ordering comparison
        __hash__: Make object hashable for use in sets and as dict keys
    """

    def __init__(self, name: str, grade: float, student_id: str):
        self.name = name
        self.grade = grade
        self.student_id = student_id

    def __str__(self) -> str:
        return f"{self.name} (Grade: {self.grade})"

    def __repr__(self) -> str:
        return f"Student('{self.name}', {self.grade}, '{self.student_id}')"

    def __eq__(self, other: "Student") -> bool:
        """Equality comparison: student1 == student2"""
        if isinstance(other, Student):
            return self.student_id == other.student_id
        return False

    def __lt__(self, other: "Student") -> bool:
        """Less than comparison: student1 < student2 (by grade)"""
        if isinstance(other, Student):
            return self.grade < other.grade
        return NotImplemented

    def __le__(self, other: "Student") -> bool:
        """Less than or equal: student1 <= student2"""
        if isinstance(other, Student):
            return self.grade <= other.grade
        return NotImplemented

    def __gt__(self, other: "Student") -> bool:
        """Greater than: student1 > student2"""
        if isinstance(other, Student):
            return self.grade > other.grade
        return NotImplemented

    def __ge__(self, other: "Student") -> bool:
        """Greater than or equal: student1 >= student2"""
        if isinstance(other, Student):
            return self.grade >= other.grade
        return NotImplemented

    def __hash__(self) -> int:
        """
        Make object hashable for use in sets and as dictionary keys.

        Objects that compare equal must have the same hash value.
        If you implement __eq__, you should also implement __hash__.
        """
        return hash(self.student_id)


# =============================================================================
# 5. Container/Sequence Operations Magic Methods
# =============================================================================


class Playlist:
    """
    Demonstrates container and sequence magic methods for custom collections.

    Magic Methods Used:
        __len__: len(obj)
        __getitem__, __setitem__, __delitem__: Indexing operations
        __contains__: 'in' operator
        __iter__: Iteration support
        __bool__: Truthiness testing
    """

    def __init__(self, name: str):
        self.name = name
        self.songs = []

    def __str__(self) -> str:
        return f"Playlist '{self.name}' with {len(self.songs)} songs"

    def __repr__(self) -> str:
        return f"Playlist('{self.name}')"

    def __len__(self) -> int:
        """Return length: len(playlist)"""
        return len(self.songs)

    def __getitem__(self, index: Union[int, slice]) -> Union[str, list]:
        """Get item by index: playlist[0] or playlist[1:3]"""
        return self.songs[index]

    def __setitem__(self, index: int, song: str) -> None:
        """Set item by index: playlist[0] = "new song" """
        self.songs[index] = song

    def __delitem__(self, index: int) -> None:
        """Delete item by index: del playlist[0]"""
        del self.songs[index]

    def __contains__(self, song: str) -> bool:
        """Check membership: "song" in playlist"""
        return song in self.songs

    def __iter__(self) -> Iterator[str]:
        """Make object iterable: for song in playlist"""
        return iter(self.songs)

    def __bool__(self) -> bool:
        """Truthiness testing: if playlist: ..."""
        return len(self.songs) > 0

    def add_song(self, song: str) -> None:
        """Add a song to the playlist."""
        self.songs.append(song)

    def remove_song(self, song: str) -> None:
        """Remove a song from the playlist."""
        self.songs.remove(song)


# =============================================================================
# 6. Attribute Access Magic Methods
# =============================================================================


class ConfigObject:
    """
    Demonstrates attribute access magic methods for dynamic attribute handling.

    Magic Methods Used:
        __getattr__: Called when attribute is not found normally
        __setattr__: Called when setting any attribute
        __delattr__: Called when deleting an attribute
        __getattribute__: Called for ALL attribute access (use carefully)
    """

    def __init__(self, **kwargs):
        # Use object.__setattr__ to avoid recursion during initialization
        object.__setattr__(self, "_data", {})
        object.__setattr__(self, "_locked", False)

        # Set initial values
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, name: str) -> Any:
        """
        Called when attribute is not found through normal lookup.

        This is only called if the attribute doesn't exist in the object's
        __dict__ or in the class hierarchy.
        """
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'ConfigObject' has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Called when setting any attribute.

        This gives you control over how attributes are set.
        Be careful to avoid infinite recursion.
        """

        # Prevent modification if locked
        if hasattr(self, "_locked") and self._locked and name not in ["_locked"]:
            raise AttributeError(f"ConfigObject is locked, cannot set '{name}'")

        # Store in _data dict instead of normal attribute storage
        if hasattr(self, "_data") and not name.startswith("_"):
            self._data[name] = value
        else:
            # Use object.__setattr__ for special attributes to avoid recursion
            object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        """Called when deleting an attribute: del obj.attr"""
        if self._locked:
            raise AttributeError("ConfigObject is locked, cannot delete attributes")

        if name in self._data:
            del self._data[name]
        else:
            object.__delattr__(self, name)

    def lock(self) -> None:
        """Lock the configuration to prevent further changes."""
        self._locked = True

    def unlock(self) -> None:
        """Unlock the configuration to allow changes."""
        self._locked = False

    def __repr__(self) -> str:
        return f"ConfigObject({self._data})"


# =============================================================================
# 7. Callable Objects Magic Methods
# =============================================================================


class Counter:
    """
    Demonstrates __call__ magic method to make objects callable like functions.

    Magic Methods Used:
        __call__: Makes object callable like a function
    """

    def __init__(self, initial_value: int = 0):
        self.value = initial_value
        self.call_count = 0

    def __call__(self, increment: int = 1) -> int:
        """
        Make the object callable: counter() or counter(5)

        This allows the object to be used like a function.
        Useful for creating function-like objects with state.
        """
        self.value += increment
        self.call_count += 1
        return self.value

    def __str__(self) -> str:
        return f"Counter(value={self.value}, calls={self.call_count})"


# =============================================================================
# 8. Context Manager Magic Methods
# =============================================================================


class FileManager:
    """
    Demonstrates context manager magic methods for 'with' statement support.

    Magic Methods Used:
        __enter__: Called when entering 'with' block
        __exit__: Called when exiting 'with' block (handles cleanup)
    """

    def __init__(self, filename: str, mode: str = "r"):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        """
        Called when entering the 'with' block.

        Should return the resource that will be used in the with block.
        """
        print(f"Opening file: {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Called when exiting the 'with' block.

        Parameters:
            exc_type: Exception type (None if no exception)
            exc_value: Exception value (None if no exception)
            traceback: Exception traceback (None if no exception)

        Return True to suppress exceptions, False to propagate them.
        """
        if self.file:
            print(f"Closing file: {self.filename}")
            self.file.close()

        if exc_type:
            print(f"Exception occurred: {exc_type.__name__}: {exc_value}")

        # Return False to propagate exceptions (don't suppress them)
        return False


# =============================================================================
# 9. Copying Magic Methods
# =============================================================================


class Document:
    """
    Demonstrates copying magic methods for custom copy behavior.

    Magic Methods Used:
        __copy__: Shallow copy behavior
        __deepcopy__: Deep copy behavior
    """

    def __init__(self, title: str, content: list):
        self.title = title
        self.content = content
        self.metadata = {"created": "2024-01-01", "version": 1}

    def __copy__(self):
        """
        Shallow copy: copy.copy(obj)

        Creates a new object but shares references to contained objects.
        """
        print("Performing shallow copy")
        new_doc = Document(self.title, self.content)  # Note: shares content list
        new_doc.metadata = self.metadata.copy()  # Shallow copy of metadata
        return new_doc

    def __deepcopy__(self, memo):
        """
        Deep copy: copy.deepcopy(obj)

        Creates a new object and recursively copies all contained objects.
        memo is used to track already copied objects to handle circular references.
        """
        print("Performing deep copy")
        new_doc = Document(
            copy.deepcopy(self.title, memo), copy.deepcopy(self.content, memo)
        )
        new_doc.metadata = copy.deepcopy(self.metadata, memo)
        return new_doc

    def __repr__(self) -> str:
        return f"Document('{self.title}', {self.content})"


# =============================================================================
# 10. Special Iterator Magic Methods
# =============================================================================


class Fibonacci:
    """
    Demonstrates iterator magic methods for custom iteration behavior.

    Magic Methods Used:
        __iter__: Returns iterator object
        __next__: Returns next item in sequence
    """

    def __init__(self, max_count: int = 10):
        self.max_count = max_count
        self.count = 0
        self.current = 0
        self.next_val = 1

    def __iter__(self):
        """Return the iterator object (self)"""
        return self

    def __next__(self):
        """Return the next Fibonacci number"""
        if self.count >= self.max_count:
            raise StopIteration

        result = self.current
        self.current, self.next_val = self.next_val, self.current + self.next_val
        self.count += 1
        return result


# =============================================================================
# Demonstration Functions
# =============================================================================


def demonstrate_object_creation():
    """Demonstrate object creation and destruction magic methods."""
    print("\n" + "=" * 60)
    print("1. Object Creation & Destruction Magic Methods")
    print("=" * 60)

    # Demonstrate __new__ singleton pattern
    print("Creating bank accounts (singleton pattern):")
    account1 = SmartBankAccount("12345", 1000.0)
    account2 = SmartBankAccount("12345", 2000.0)  # Same account number
    account3 = SmartBankAccount("67890", 500.0)  # Different account number

    print(f"account1 is account2: {account1 is account2}")  # True
    print(f"account1 is account3: {account1 is account3}")  # False
    print(f"Account 1 balance: ${account1.balance}")
    print(f"Account 2 balance: ${account2.balance}")  # Same as account1


def demonstrate_string_representation():
    """Demonstrate string representation magic methods."""

    print("\n" + "=" * 60)
    print("2. String Representation Magic Methods")
    print("=" * 60)

    product = Product("Laptop", 999.99, "Electronics")

    print(f"str(product): {str(product)}")
    print(f"repr(product): {repr(product)}")
    print(f"Short format: {product:short}")
    print(f"Detailed format: {product:detailed}")
    print(f"Price format: {product:price}")


def demonstrate_arithmetic_operations():
    """Demonstrate arithmetic magic methods."""
    print("\n" + "=" * 60)
    print("3. Arithmetic Operations Magic Methods")
    print("=" * 60)

    v1 = Vector(3, 4)
    v2 = Vector(1, 2)

    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 2 = {v1 * 2}")
    print(f"3 * v1 = {3 * v1}")
    print(f"v1 / 2 = {v1 / 2}")
    print(f"-v1 = {-v1}")
    print(f"abs(v1) = {abs(v1)}")
    print(f"v1 ** 2 = {v1**2}")

    # In-place operations
    v1 += v2
    print(f"After v1 += v2: v1 = {v1}")


def demonstrate_comparison_operations():
    """Demonstrate comparison magic methods."""
    print("\n" + "=" * 60)
    print("4. Comparison Operations Magic Methods")
    print("=" * 60)

    students = [
        Student("Alice", 85.5, "S001"),
        Student("Bob", 92.0, "S002"),
        Student("Charlie", 78.5, "S003"),
        Student("Diana", 96.5, "S004"),
    ]

    print("Original students:")
    for student in students:
        print(f"  {student}")

    # Sorting works because we implemented comparison methods
    students.sort()
    print("\nSorted by grade (ascending):")
    for student in students:
        print(f"  {student}")

    # Equality and hashing
    alice1 = Student("Alice", 85.5, "S001")
    alice2 = Student("Alice Johnson", 90.0, "S001")  # Same ID, different name/grade
    print(f"\nEquality test (same student ID):")
    print(f"alice1 == alice2: {alice1 == alice2}")
    print(f"hash(alice1) == hash(alice2): {hash(alice1) == hash(alice2)}")

    # Using in sets
    student_set = {alice1, alice2}  # Should have only one student (same ID)
    print(f"Set with both Alices: {len(student_set)} student(s)")


def demonstrate_container_operations():
    """Demonstrate container and sequence magic methods."""
    print("\n" + "=" * 60)
    print("5. Container/Sequence Operations Magic Methods")
    print("=" * 60)

    playlist = Playlist("My Favorites")

    # Add songs
    playlist.add_song("Bohemian Rhapsody")
    playlist.add_song("Stairway to Heaven")
    playlist.add_song("Hotel California")

    print(f"Playlist: {playlist}")
    print(f"Length: {len(playlist)}")
    print(f"First song: {playlist[0]}")
    print(f"Last two songs: {playlist[1:3]}")

    # Membership testing
    print(f"'Bohemian Rhapsody' in playlist: {'Bohemian Rhapsody' in playlist}")
    print(f"'Yesterday' in playlist: {'Yesterday' in playlist}")

    # Iteration
    print("All songs:")
    for i, song in enumerate(playlist, 1):
        print(f"  {i}. {song}")

    # Truthiness
    empty_playlist = Playlist("Empty")
    print(f"Playlist is truthy: {bool(playlist)}")
    print(f"Empty playlist is truthy: {bool(empty_playlist)}")

    # Modification
    playlist[1] = "Imagine"
    print(f"After changing song 2: {playlist[1]}")


def demonstrate_attribute_access():
    """Demonstrate attribute access magic methods."""

    print("\n" + "=" * 60)
    print("6. Attribute Access Magic Methods")
    print("=" * 60)

    # Create configuration object
    config = ConfigObject(debug=True, port=8080, host="localhost")
    print(f"Initial config: {config}")

    # Dynamic attribute access
    config.database_url = "postgresql://localhost/mydb"
    config.max_connections = 100

    print(f"After adding attributes: {config}")
    print(f"Debug mode: {config.debug}")
    print(f"Database URL: {config.database_url}")

    # Lock configuration
    config.lock()
    print("Configuration locked")

    try:
        config.new_setting = "this will fail"
    except AttributeError as e:
        print(f"Error setting locked attribute: {e}")

    # Unlock and modify
    config.unlock()
    config.new_setting = "this works now"
    print(f"After unlocking: {config}")


def demonstrate_callable_objects():
    """Demonstrate callable objects magic method."""

    print("\n" + "=" * 60)
    print("7. Callable Objects Magic Method")
    print("=" * 60)

    # Create counter object
    counter = Counter(10)
    print(f"Initial counter: {counter}")

    # Call the object like a function
    result1 = counter()  # Default increment of 1
    result2 = counter(5)  # Increment by 5
    result3 = counter(-2)  # Decrement by 2

    print(f"After counter(): {result1}, counter state: {counter}")
    print(f"After counter(5): {result2}, counter state: {counter}")
    print(f"After counter(-2): {result3}, counter state: {counter}")


def demonstrate_context_managers():
    """Demonstrate context manager magic methods."""

    print("\n" + "=" * 60)
    print("8. Context Manager Magic Methods")
    print("=" * 60)

    # Create a test file first
    with open("test_file.txt", "w") as f:
        f.write("Hello, World!\nThis is a test file.")

    # Use custom context manager
    print("Using custom FileManager:")
    try:
        with FileManager("test_file.txt", "r") as file:
            content = file.read()
            print(f"File content: {content[:30]}...")
    except Exception as e:
        print(f"Error: {e}")

    # Demonstrate exception handling
    print("\nTesting with non-existent file:")
    try:
        with FileManager("non_existent.txt", "r") as file:
            content = file.read()
    except FileNotFoundError as e:
        print(f"Caught exception: {e}")


def demonstrate_copying():
    """Demonstrate copying magic methods."""
    print("\n" + "=" * 60)
    print("9. Copying Magic Methods")
    print("=" * 60)

    # Create original document
    original = Document("My Document", ["Chapter 1", "Chapter 2"])
    print(f"Original: {original}")

    # Shallow copy
    shallow = copy.copy(original)
    print(f"Shallow copy: {shallow}")

    # Deep copy
    deep = copy.deepcopy(original)
    print(f"Deep copy: {deep}")

    # Modify original content list
    original.content.append("Chapter 3")
    print(f"\nAfter modifying original content:")
    print(f"Original: {original}")
    print(f"Shallow copy: {shallow}")  # Shares content list
    print(f"Deep copy: {deep}")  # Independent content list

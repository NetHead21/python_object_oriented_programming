# **Protocol vs ABC Overview**

# | Aspect | **Protocol** | **abc.ABC** |
# |--------|-------------|-------------|
# | **Type** | Structural typing (duck typing) | Nominal typing (inheritance) |
# | **Enforcement** | Static type checking only | Runtime enforcement |
# | **Inheritance** | No inheritance required | Must inherit from ABC |
# | **When checked** | Type checker (mypy, etc.) | Runtime when methods called |
# | **Flexibility** | Very flexible | More rigid |

## **Protocol (Structural Typing)**

## **What it is:**
# - Defines an interface based on **structure** (what methods/attributes exist)
# - No inheritance required - if it "looks like a duck and quacks like a duck"
# - Only enforced by static type checkers (mypy, PyCharm, VS Code)
### **Example:**
from typing import Protocol


class Drawable(Protocol):
    """Protocol for objects that can be drawn."""

    def draw(self) -> None:
        """Draw the object."""
        ...

    def get_area(self) -> float:
        """Get the area of the object."""
        ...


# No inheritance needed - just implement the methods
class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> None:
        print(f"Drawing circle with radius {self.radius}")

    def get_area(self) -> float:
        return 3.14159 * self.radius**2


class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def draw(self) -> None:
        print(f"Drawing rectangle {self.width}x{self.height}")

    def get_area(self) -> float:
        return self.width * self.height


# Both Circle and Rectangle automatically satisfy the Drawable protocol
def render_shape(shape: Drawable) -> None:
    """Render any drawable shape."""
    shape.draw()
    print(f"Area: {shape.get_area()}")


# Works without explicit inheritance
circle = Circle(5)
rectangle = Rectangle(10, 20)

render_shape(circle)  # ✅ Works
render_shape(rectangle)  # ✅ Works


## **abc.ABC (Abstract Base Classes)**

### **What it is:**
# - Defines an interface through **inheritance**
# - Runtime enforcement - methods must be implemented
# - Raises `TypeError` at instantiation if abstract methods not implemented
### **Example:**
from abc import ABC, abstractmethod


class Drawable(ABC):
    """Abstract base class for drawable objects."""

    @abstractmethod
    def draw(self) -> None:
        """Draw the object."""
        pass

    @abstractmethod
    def get_area(self) -> float:
        """Get the area of the object."""
        pass

    # Can have concrete methods too
    def describe(self) -> str:
        """Describe the object."""
        return f"This shape has area {self.get_area()}"


# Must inherit from Drawable
class Circle(Drawable):
    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> None:
        print(f"Drawing circle with radius {self.radius}")

    def get_area(self) -> float:
        return 3.14159 * self.radius**2


class Rectangle(Drawable):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def draw(self) -> None:
        print(f"Drawing rectangle {self.width}x{self.height}")

    def get_area(self) -> float:
        return self.width * self.height


# This would raise TypeError at runtime
# class BrokenShape(Drawable):
#     pass
#
# broken = BrokenShape()  # TypeError: Can't instantiate abstract class


def render_shape(shape: Drawable) -> None:
    """Render any drawable shape."""
    shape.draw()
    print(shape.describe())


circle = Circle(5)
rectangle = Rectangle(10, 20)

render_shape(circle)  # ✅ Works
render_shape(rectangle)  # ✅ Works


## **Real-World Example: Socket Server Interface**

# Let's apply this to your socket server:

### **Using Protocol:**
from typing import Protocol


class SocketLike(Protocol):
    """Protocol for socket-like objects."""

    def recv(self, count: int) -> bytes:
        """Receive data from the socket."""
        ...

    def send(self, data: bytes) -> None:
        """Send data through the socket."""
        ...

    def close(self) -> None:
        """Close the socket."""
        ...


# Your LogSocket automatically satisfies the protocol
class LogSocket:
    def __init__(self, socket):
        self.socket = socket

    def recv(self, count: int) -> bytes:
        data = self.socket.recv(count)
        print(f"Received: {data!r}")
        return data

    def send(self, data: bytes) -> None:
        print(f"Sending: {data!r}")
        self.socket.send(data)

    def close(self) -> None:
        self.socket.close()


# Works with any socket-like object
def dice_response(client: SocketLike) -> None:
    """Handle dice request - works with any socket-like object."""
    request = client.recv(1024)
    # ... process request
    client.send(b"response")


# Both work automatically
import socket

real_socket = socket.socket()
log_socket = LogSocket(real_socket)

dice_response(real_socket)  # ✅ Works
dice_response(log_socket)  # ✅ Works


### **Using ABC:**
from abc import ABC, abstractmethod


class SocketInterface(ABC):
    """Abstract interface for socket-like objects."""

    @abstractmethod
    def recv(self, count: int) -> bytes:
        """Receive data from the socket."""
        pass

    @abstractmethod
    def send(self, data: bytes) -> None:
        """Send data through the socket."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the socket."""
        pass


# Must inherit from SocketInterface
class LogSocket(SocketInterface):
    def __init__(self, socket):
        self.socket = socket

    def recv(self, count: int) -> bytes:
        data = self.socket.recv(count)
        print(f"Received: {data!r}")
        return data

    def send(self, data: bytes) -> None:
        print(f"Sending: {data!r}")
        self.socket.send(data)

    def close(self) -> None:
        self.socket.close()


# Need wrapper for regular socket
class SocketWrapper(SocketInterface):
    def __init__(self, socket):
        self.socket = socket

    def recv(self, count: int) -> bytes:
        return self.socket.recv(count)

    def send(self, data: bytes) -> None:
        self.socket.send(data)

    def close(self) -> None:
        self.socket.close()


def dice_response(client: SocketInterface) -> None:
    """Handle dice request - requires SocketInterface inheritance."""
    request = client.recv(1024)
    # ... process request
    client.send(b"response")


## **When to Use Protocol**


### **✅ Use Protocol when:**
# - Working with **existing classes** you can't modify
# - Want **flexibility** without forcing inheritance
# - **Duck typing** is sufficient
# - Working with **third-party libraries**
# - Type checking is your main concern


### **Example scenarios:**
# File-like objects
class FileLike(Protocol):
    def read(self) -> str: ...
    def write(self, data: str) -> None: ...


# Works with built-in files, StringIO, custom classes, etc.
def process_file(file: FileLike) -> None:
    content = file.read()
    file.write("processed")


# Iterable protocol
class Iterable(Protocol):
    def __iter__(self): ...


# Works with lists, sets, custom iterables, etc.


## **When to Use ABC**


### **✅ Use ABC when:**
# - You control the **class hierarchy**
# - Need **runtime enforcement**
# - Want to provide **shared implementation**
# - Building a **framework** or **library**
# - Need **stronger contracts**


### **Example scenarios:**
# Plugin system
class Plugin(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    def get_version(self) -> str:
        return "1.0"  # Shared implementation


# Database backends
class DatabaseBackend(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def query(self, sql: str) -> list:
        pass

    def close(self) -> None:
        # Default implementation
        pass

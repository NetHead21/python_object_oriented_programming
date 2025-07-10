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

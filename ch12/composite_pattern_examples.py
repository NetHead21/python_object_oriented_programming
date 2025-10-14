"""
Composite Design Pattern - Comprehensive Examples and Implementation Guide

This module provides extensive examples of the Composite design pattern,
demonstrating its application across multiple domains including file systems,
organization structures, UI components, and mathematical expressions.

PATTERN OVERVIEW:
================
The Composite Pattern is a structural design pattern that composes objects into
tree structures to represent part-whole hierarchies. It lets clients treat
individual objects and compositions of objects uniformly.

Key characteristics:
- Tree structure representation
- Uniform treatment of individual and composite objects
- Recursive composition capabilities
- Simplified client code

PATTERN STRUCTURE:
==================
- Component: Common interface/abstract class for all objects in the composition
- Leaf: Represents end objects that have no children (terminal nodes)
- Composite: Defines behavior for components having children and stores child components
- Client: Manipulates objects in the composition through the Component interface

WHEN TO USE:
============
✅ You want to represent part-whole hierarchies of objects
✅ You want clients to ignore differences between compositions and individual objects
✅ You need to work with tree-like structures
✅ You want to add functionality uniformly across the structure

REAL-WORLD EXAMPLES:
====================
- File systems (files and directories)
- Organization charts (employees and departments)
- GUI components (buttons, panels, windows)
- Mathematical expressions (numbers and operators)
- Menu systems (items and submenus)
- Graphics systems (shapes and groups)
"""

from abc import ABC, abstractmethod
from typing import List, Optional
import math


# =============================================================================
# Example 1: File System Hierarchy
# =============================================================================


class FileSystemComponent(ABC):
    """Abstract component for file system objects.

    This is the base component that defines the common interface for both
    files (leaf objects) and directories (composite objects). It establishes
    the contract that all file system objects must follow.

    The interface supports both individual operations (like getting size)
    and composite operations (like adding/removing children). Not all
    operations are meaningful for all types - for example, files can't
    have children added to them.
    """

    def __init__(self, name: str):
        """Initialize the file system component with a name.

        Args:
            name (str): The name of the file or directory
        """
        self.name = name
        self.parent: Optional["FileSystemComponent"] = None

    @abstractmethod
    def get_size(self) -> int:
        """Get the size of this component in bytes.

        For files, this returns the actual file size.
        For directories, this recursively calculates the total size
        of all contained files and subdirectories.

        Returns:
            int: Size in bytes
        """
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        """Display the component with proper indentation for tree structure.

        Args:
            indent (int): Current indentation level for tree display

        Returns:
            str: Formatted string representation of the component
        """
        pass

    def add(self, component: "FileSystemComponent") -> None:
        """Add a child component (only meaningful for directories).

        Args:
            component: The component to add as a child

        Raises:
            NotImplementedError: For leaf components that can't have children
        """
        raise NotImplementedError("Cannot add to a leaf component")

    def remove(self, component: "FileSystemComponent") -> None:
        """Remove a child component (only meaningful for directories).

        Args:
            component: The component to remove

        Raises:
            NotImplementedError: For leaf components that don't have children
        """
        raise NotImplementedError("Cannot remove from a leaf component")

    def get_children(self) -> List["FileSystemComponent"]:
        """Get list of child components (only meaningful for directories).

        Returns:
            List: Empty list for leaf components
        """
        return []

    def find(self, name: str) -> Optional["FileSystemComponent"]:
        """Find a component by name in the tree structure.

        Args:
            name (str): Name of the component to find

        Returns:
            Optional[FileSystemComponent]: Found component or None
        """
        if self.name == name:
            return self
        return None

    def get_path(self) -> str:
        """Get the full path of this component.

        Returns:
            str: Full path from root to this component
        """
        if self.parent is None:
            return self.name
        return f"{self.parent.get_path()}/{self.name}"


class File(FileSystemComponent):
    """Leaf component representing a file in the file system.

    Files are terminal nodes in the file system tree - they cannot contain
    other components. They have a specific size and content type.
    """

    def __init__(self, name: str, size: int, content_type: str = "text"):
        """Initialize a file with name, size, and content type.

        Args:
            name (str): File name including extension
            size (int): File size in bytes
            content_type (str): Type of content (text, binary, image, etc.)
        """
        super().__init__(name)
        self.size = size
        self.content_type = content_type

    def get_size(self) -> int:
        """Get the file size.

        Returns:
            int: File size in bytes
        """
        return self.size

    def display(self, indent: int = 0) -> str:
        """Display the file with proper indentation and details.

        Args:
            indent (int): Current indentation level

        Returns:
            str: Formatted file representation
        """
        prefix = "  " * indent
        size_kb = self.size / 1024
        return f"{prefix}📄 {self.name} ({size_kb:.1f} KB, {self.content_type})"

    def get_content_preview(self, chars: int = 50) -> str:
        """Get a preview of the file content (simulated).

        Args:
            chars (int): Number of characters to preview

        Returns:
            str: Simulated content preview
        """

        if self.content_type == "text":
            return f"Sample text content from {self.name}..."[:chars]
        elif self.content_type == "image":
            return f"[Image data: {self.name}]"
        else:
            return f"[Binary data: {self.size} bytes]"


class Directory(FileSystemComponent):
    """Composite component representing a directory in the file system.

    Directories can contain other directories and files, forming a tree
    structure. They implement the composite operations for managing children.
    """

    def __init__(self, name: str):
        """Initialize an empty directory.

        Args:
            name (str): Directory name
        """
        super().__init__(name)
        self.children: List[FileSystemComponent] = []

    def add(self, component: FileSystemComponent) -> None:
        """Add a file or subdirectory to this directory.

        Args:
            component: File or Directory to add
        """
        component.parent = self
        self.children.append(component)

    def remove(self, component: FileSystemComponent) -> None:
        """Remove a file or subdirectory from this directory.

        Args:
            component: File or Directory to remove
        """
        if component in self.children:
            component.parent = None
            self.children.remove(component)

    def get_children(self) -> List[FileSystemComponent]:
        """Get all direct children of this directory.

        Returns:
            List[FileSystemComponent]: List of files and subdirectories
        """
        return self.children.copy()

    def get_size(self) -> int:
        """Get the total size of the directory and all its contents.

        This recursively calculates the size by summing all contained
        files and subdirectories.

        Returns:
            int: Total size in bytes
        """
        total_size = 0
        for child in self.children:
            total_size += child.get_size()
        return total_size

    def display(self, indent: int = 0) -> str:
        """Display the directory tree with proper indentation.

        Args:
            indent (int): Current indentation level

        Returns:
            str: Formatted directory tree representation
        """
        prefix = "  " * indent
        result = f"{prefix}📁 {self.name}/ ({len(self.children)} items, {self.get_size() / 1024:.1f} KB total)\n"

        for child in sorted(self.children, key=lambda x: (isinstance(x, File), x.name)):
            result += child.display(indent + 1) + "\n"

        return result.rstrip()

    def find(self, name: str) -> Optional[FileSystemComponent]:
        """Find a component by name in this directory tree.

        Args:
            name (str): Name to search for

        Returns:
            Optional[FileSystemComponent]: Found component or None
        """
        if self.name == name:
            return self

        for child in self.children:
            found = child.find(name)
            if found:
                return found

        return None

    def get_file_count(self) -> int:
        """Get the total number of files in this directory tree.

        Returns:
            int: Total number of files (excluding directories)
        """
        count = 0
        for child in self.children:
            if isinstance(child, File):
                count += 1
            elif isinstance(child, Directory):
                count += child.get_file_count()
        return count

    def get_directory_count(self) -> int:
        """Get the total number of subdirectories in this directory tree.

        Returns:
            int: Total number of subdirectories
        """
        count = 0
        for child in self.children:
            if isinstance(child, Directory):
                count += 1 + child.get_directory_count()
        return count


# =============================================================================
# Example 2: Organization Structure
# =============================================================================


class OrganizationComponent(ABC):
    """Abstract component for organizational hierarchy.

    This defines the common interface for both individual employees
    and organizational units (departments, teams, etc.).
    """

    def __init__(self, name: str, title: str):
        """Initialize an organizational component.

        Args:
            name (str): Name of the person or unit
            title (str): Title or designation
        """
        self.name = name
        self.title = title
        self.manager: Optional["OrganizationComponent"] = None

    @abstractmethod
    def get_salary_cost(self) -> float:
        """Get the total salary cost for this component.

        Returns:
            float: Total salary cost
        """
        pass

    @abstractmethod
    def get_headcount(self) -> int:
        """Get the total number of people in this component.

        Returns:
            int: Number of people
        """
        pass

    @abstractmethod
    def display_hierarchy(self, indent: int = 0) -> str:
        """Display the organizational hierarchy.

        Args:
            indent (int): Indentation level

        Returns:
            str: Formatted hierarchy display
        """
        pass

    def add_report(self, component: "OrganizationComponent") -> None:
        """Add a direct report (only for managers/departments).

        Args:
            component: The component to add as a direct report
        """
        raise NotImplementedError("Cannot add reports to individual employees")

    def remove_report(self, component: "OrganizationComponent") -> None:
        """Remove a direct report (only for managers/departments).

        Args:
            component: The component to remove
        """
        raise NotImplementedError("Cannot remove reports from individual employees")

    def get_reports(self) -> List["OrganizationComponent"]:
        """Get all direct reports.

        Returns:
            List: Empty list for individual employees
        """
        return []


class Employee(OrganizationComponent):
    """Leaf component representing an individual employee.

    Employees are terminal nodes in the organizational hierarchy.
    They have specific salary, department, and skill information.
    """

    def __init__(
        self,
        name: str,
        title: str,
        salary: float,
        department: str = "",
        skills: List[str] = None,
    ):
        """Initialize an employee.

        Args:
            name (str): Employee name
            title (str): Job title
            salary (float): Annual salary
            department (str): Department name
            skills (List[str]): List of skills
        """
        super().__init__(name, title)
        self.salary = salary
        self.department = department
        self.skills = skills or []

    def get_salary_cost(self) -> float:
        """Get the employee's salary.

        Returns:
            float: Annual salary
        """
        return self.salary

    def get_headcount(self) -> int:
        """Individual employee counts as 1.

        Returns:
            int: Always returns 1
        """
        return 1

    def display_hierarchy(self, indent: int = 0) -> str:
        """Display employee information with indentation.

        Args:
            indent (int): Indentation level

        Returns:
            str: Formatted employee display
        """
        prefix = "  " * indent
        return (
            f"{prefix}👤 {self.name} - {self.title} "
            f"(${self.salary:,.0f}/year, {self.department})"
        )

    def get_skills_summary(self) -> str:
        """Get a summary of the employee's skills.

        Returns:
            str: Comma-separated list of skills
        """
        return ", ".join(self.skills) if self.skills else "No skills listed"


class Department(OrganizationComponent):
    """Composite component representing a department or team.

    Departments can contain employees and other departments,
    forming a hierarchical organizational structure.
    """

    def __init__(self, name: str, title: str = "Department", budget: float = 0.0):
        """Initialize a department.

        Args:
            name (str): Department name
            title (str): Department title/type
            budget (float): Annual budget
        """
        super().__init__(name, title)
        self.budget = budget
        self.members: List[OrganizationComponent] = []

    def add_report(self, component: OrganizationComponent) -> None:
        """Add an employee or subdepartment to this department.

        Args:
            component: Employee or Department to add
        """
        component.manager = self
        self.members.append(component)

    def remove_report(self, component: OrganizationComponent) -> None:
        """Remove an employee or subdepartment from this department.

        Args:
            component: Employee or Department to remove
        """
        if component in self.members:
            component.manager = None
            self.members.remove(component)

    def get_reports(self) -> List[OrganizationComponent]:
        """Get all direct reports in this department.

        Returns:
            List[OrganizationComponent]: List of employees and subdepartments
        """
        return self.members.copy()

    def get_salary_cost(self) -> float:
        """Get the total salary cost for the entire department.

        Returns:
            float: Total salary cost including all subdepartments
        """
        total_cost = 0.0
        for member in self.members:
            total_cost += member.get_salary_cost()
        return total_cost

    def get_headcount(self) -> int:
        """Get the total number of people in the department.

        Returns:
            int: Total headcount including subdepartments
        """
        total_count = 0
        for member in self.members:
            total_count += member.get_headcount()
        return total_count

    def display_hierarchy(self, indent: int = 0) -> str:
        """Display the department hierarchy with all members.

        Args:
            indent (int): Indentation level

        Returns:
            str: Formatted department hierarchy
        """
        prefix = "  " * indent
        result = (
            f"{prefix}🏢 {self.name} ({self.title}) - "
            f"{self.get_headcount()} people, "
            f"${self.get_salary_cost():,.0f} total cost\n"
        )

        # Sort members: departments first, then employees by name
        sorted_members = sorted(
            self.members, key=lambda x: (isinstance(x, Employee), x.name)
        )

        for member in sorted_members:
            result += member.display_hierarchy(indent + 1) + "\n"

        return result.rstrip()

    def get_budget_utilization(self) -> float:
        """Calculate budget utilization percentage.

        Returns:
            float: Percentage of budget used by salary costs
        """
        if self.budget == 0:
            return 0.0
        return (self.get_salary_cost() / self.budget) * 100

    def find_employee(self, name: str) -> Optional[Employee]:
        """Find an employee by name in the department hierarchy.

        Args:
            name (str): Employee name to search for

        Returns:
            Optional[Employee]: Found employee or None
        """
        for member in self.members:
            if isinstance(member, Employee) and member.name == name:
                return member
            elif isinstance(member, Department):
                found = member.find_employee(name)
                if found:
                    return found
        return None


# =============================================================================
# Example 3: UI Component System
# =============================================================================


class UIComponent(ABC):
    """Abstract component for UI elements.

    This defines the common interface for both individual UI elements
    (buttons, labels) and container elements (panels, windows).
    """

    def __init__(
        self, name: str, x: int = 0, y: int = 0, width: int = 100, height: int = 50
    ):
        """Initialize a UI component with position and size.

        Args:
            name (str): Component name/identifier
            x (int): X position
            y (int): Y position
            width (int): Component width
            height (int): Component height
        """
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        self.parent: Optional["UIComponent"] = None

    @abstractmethod
    def render(self, indent: int = 0) -> str:
        """Render the component for display.

        Args:
            indent (int): Indentation level for nested display

        Returns:
            str: Rendered component representation
        """
        pass

    @abstractmethod
    def get_bounds(self) -> tuple:
        """Get the bounding rectangle of the component.

        Returns:
            tuple: (x, y, width, height) bounds
        """
        pass

    def add_child(self, component: "UIComponent") -> None:
        """Add a child component (only for containers).

        Args:
            component: Child component to add
        """
        raise NotImplementedError("Cannot add children to leaf components")

    def remove_child(self, component: "UIComponent") -> None:
        """Remove a child component (only for containers).

        Args:
            component: Child component to remove
        """
        raise NotImplementedError("Cannot remove children from leaf components")

    def get_children(self) -> List["UIComponent"]:
        """Get all child components.

        Returns:
            List: Empty list for leaf components
        """
        return []

    def set_visible(self, visible: bool) -> None:
        """Set the visibility of this component and all children.

        Args:
            visible (bool): Whether component should be visible
        """
        self.visible = visible

    def move(self, dx: int, dy: int) -> None:
        """Move the component by the specified offset.

        Args:
            dx (int): X offset
            dy (int): Y offset
        """
        self.x += dx
        self.y += dy


class Button(UIComponent):
    """Leaf component representing a UI button.

    Buttons are terminal UI elements that can be clicked but
    cannot contain other components.
    """

    def __init__(
        self,
        name: str,
        text: str,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 30,
    ):
        """Initialize a button with text and styling.

        Args:
            name (str): Button identifier
            text (str): Button text/label
            x (int): X position
            y (int): Y position
            width (int): Button width
            height (int): Button height
        """
        super().__init__(name, x, y, width, height)
        self.text = text
        self.enabled = True
        self.style = "default"

    def render(self, indent: int = 0) -> str:
        """Render the button with its current state.

        Args:
            indent (int): Indentation level

        Returns:
            str: Button rendering representation
        """
        prefix = "  " * indent
        status = "enabled" if self.enabled else "disabled"
        visibility = "visible" if self.visible else "hidden"
        return (
            f"{prefix}🔘 Button '{self.text}' at ({self.x}, {self.y}) "
            f"[{self.width}x{self.height}] - {status}, {visibility}"
        )

    def get_bounds(self) -> tuple:
        """Get the button's bounding rectangle.

        Returns:
            tuple: (x, y, width, height)
        """
        return (self.x, self.y, self.width, self.height)

    def click(self) -> str:
        """Simulate button click action.

        Returns:
            str: Click action description
        """
        if self.enabled and self.visible:
            return f"Button '{self.text}' clicked!"
        else:
            return f"Button '{self.text}' cannot be clicked (disabled or hidden)"


class Label(UIComponent):
    """Leaf component representing a UI label.

    Labels display text and are terminal UI elements.
    """

    def __init__(
        self,
        name: str,
        text: str,
        x: int = 0,
        y: int = 0,
        width: int = 100,
        height: int = 20,
    ):
        """Initialize a label with text content.

        Args:
            name (str): Label identifier
            text (str): Label text content
            x (int): X position
            y (int): Y position
            width (int): Label width
            height (int): Label height
        """
        super().__init__(name, x, y, width, height)
        self.text = text
        self.font_size = 12
        self.color = "black"

    def render(self, indent: int = 0) -> str:
        """Render the label with its text.

        Args:
            indent (int): Indentation level

        Returns:
            str: Label rendering representation
        """

        prefix = "  " * indent
        visibility = "visible" if self.visible else "hidden"
        return (
            f"{prefix}🏷️  Label '{self.text}' at ({self.x}, {self.y}) "
            f"[{self.width}x{self.height}] - {visibility}"
        )

    def get_bounds(self) -> tuple:
        """Get the label's bounding rectangle.

        Returns:
            tuple: (x, y, width, height)
        """
        return (self.x, self.y, self.width, self.height)

    def set_text(self, text: str) -> None:
        """Update the label text.

        Args:
            text (str): New text content
        """
        self.text = text


class Panel(UIComponent):
    """Composite component representing a UI panel/container.

    Panels can contain other UI components (buttons, labels, other panels)
    and manage their layout and rendering.
    """

    def __init__(
        self, name: str, x: int = 0, y: int = 0, width: int = 200, height: int = 150
    ):
        """Initialize a panel container.

        Args:
            name (str): Panel identifier
            x (int): X position
            y (int): Y position
            width (int): Panel width
            height (int): Panel height
        """
        super().__init__(name, x, y, width, height)
        self.children: List[UIComponent] = []
        self.background_color = "lightgray"
        self.border = True

    def add_child(self, component: UIComponent) -> None:
        """Add a child component to this panel.

        Args:
            component: UI component to add as child
        """
        component.parent = self
        self.children.append(component)

    def remove_child(self, component: UIComponent) -> None:
        """Remove a child component from this panel.

        Args:
            component: UI component to remove
        """
        if component in self.children:
            component.parent = None
            self.children.remove(component)

    def get_children(self) -> List[UIComponent]:
        """Get all child components.

        Returns:
            List[UIComponent]: List of child components
        """
        return self.children.copy()

    def render(self, indent: int = 0) -> str:
        """Render the panel and all its children.

        Args:
            indent (int): Indentation level

        Returns:
            str: Panel rendering representation
        """
        prefix = "  " * indent
        visibility = "visible" if self.visible else "hidden"
        result = (
            f"{prefix}📦 Panel '{self.name}' at ({self.x}, {self.y}) "
            f"[{self.width}x{self.height}] - {len(self.children)} children, {visibility}\n"
        )
        for child in self.children:
            result += child.render(indent + 1) + "\n"

        return result.rstrip()

    def get_bounds(self) -> tuple:
        """Get the panel's bounding rectangle.

        Returns:
            tuple: (x, y, width, height)
        """
        return (self.x, self.y, self.width, self.height)

    def set_visible(self, visible: bool) -> None:
        """Set visibility of panel and all children.

        Args:
            visible (bool): Whether panel should be visible
        """
        self.visible = visible
        for child in self.children:
            child.set_visible(visible)

    def move(self, dx: int, dy: int) -> None:
        """Move panel and all children by offset.

        Args:
            dx (int): X offset
            dy (int): Y offset
        """
        super().move(dx, dy)
        for child in self.children:
            child.move(dx, dy)

    def find_component(self, name: str) -> Optional[UIComponent]:
        """Find a component by name in the panel hierarchy.

        Args:
            name (str): Component name to search for

        Returns:
            Optional[UIComponent]: Found component or None
        """
        if self.name == name:
            return self

        for child in self.children:
            if child.name == name:
                return child
            if isinstance(child, Panel):
                found = child.find_component(name)
                if found:
                    return found

        return None

    def get_total_components(self) -> int:
        """Get total number of components in this panel tree.

        Returns:
            int: Total component count including this panel
        """
        count = 1  # This panel
        for child in self.children:
            if isinstance(child, Panel):
                count += child.get_total_components()
            else:
                count += 1
        return count


# =============================================================================
# Example 4: Mathematical Expression Tree
# =============================================================================


class MathExpression(ABC):
    """Abstract component for mathematical expressions.

    This defines the common interface for both numbers (leaf nodes)
    and operations (composite nodes) in mathematical expression trees.
    """

    @abstractmethod
    def evaluate(self) -> float:
        """Evaluate the expression to get its numeric value.

        Returns:
            float: The calculated result
        """
        pass

    @abstractmethod
    def to_string(self) -> str:
        """Convert the expression to its string representation.

        Returns:
            str: String representation of the expression
        """
        pass

    @abstractmethod
    def get_complexity(self) -> int:
        """Get the complexity score of the expression.

        Returns:
            int: Complexity score (number of operations)
        """
        pass


class Number(MathExpression):
    """Leaf component representing a numeric value.

    Numbers are terminal nodes in mathematical expression trees.
    """

    def __init__(self, value: float):
        """Initialize a number with a specific value.

        Args:
            value (float): The numeric value
        """
        self.value = value

    def evaluate(self) -> float:
        """Get the numeric value.

        Returns:
            float: The number's value
        """
        return self.value

    def to_string(self) -> str:
        """Get string representation of the number.

        Returns:
            str: String representation
        """
        if self.value == int(self.value):
            return str(int(self.value))
        return str(self.value)

    def get_complexity(self) -> int:
        """Numbers have complexity 0 (no operations).

        Returns:
            int: Always returns 0
        """
        return 0


class BinaryOperation(MathExpression):
    """Composite component representing a binary mathematical operation.

    Binary operations have two operands (left and right) and an operator.
    They can contain numbers or other operations, forming expression trees.
    """

    def __init__(self, left: MathExpression, operator: str, right: MathExpression):
        """Initialize a binary operation.

        Args:
            left (MathExpression): Left operand
            operator (str): Operation symbol (+, -, *, /, ^)
            right (MathExpression): Right operand
        """
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self) -> float:
        """Evaluate the binary operation.

        Returns:
            float: Result of the operation

        Raises:
            ValueError: For unsupported operators
            ZeroDivisionError: For division by zero
        """

        left_val = self.left.evaluate()
        right_val = self.right.evaluate()

        if self.operator == "+":
            return left_val + right_val
        elif self.operator == "-":
            return left_val - right_val
        elif self.operator == "*":
            return left_val * right_val
        elif self.operator == "/":
            if right_val == 0:
                raise ZeroDivisionError("Division by zero")
            return left_val / right_val
        elif self.operator == "^":
            return left_val**right_val
        else:
            raise ValueError(f"Unsupported operator: {self.operator}")

    def to_string(self) -> str:
        """Get string representation of the operation.

        Returns:
            str: Infix notation with parentheses
        """
        left_str = self.left.to_string()
        right_str = self.right.to_string()

        # Add parentheses for clarity in complex expressions
        if isinstance(self.left, BinaryOperation):
            left_str = f"({left_str})"
        if isinstance(self.right, BinaryOperation):
            right_str = f"({right_str})"

        return f"{left_str} {self.operator} {right_str}"

    def get_complexity(self) -> int:
        """Get the complexity of the operation tree.

        Returns:
            int: 1 plus the complexity of both operands
        """
        return 1 + self.left.get_complexity() + self.right.get_complexity()


class UnaryOperation(MathExpression):
    """Composite component representing a unary mathematical operation.

    Unary operations have one operand and an operator (like negation, sqrt).
    """

    def __init__(self, operator: str, operand: MathExpression):
        """Initialize a unary operation.

        Args:
            operator (str): Operation symbol (-, sqrt, abs)
            operand (MathExpression): The operand
        """
        self.operator = operator
        self.operand = operand

    def evaluate(self) -> float:
        """Evaluate the unary operation.

        Returns:
            float: Result of the operation

        Raises:
            ValueError: For unsupported operators or invalid operations
        """

        operand_val = self.operand.evaluate()

        if self.operator == "-":
            return -operand_val
        elif self.operator == "sqrt":
            if operand_val < 0:
                raise ValueError("Cannot take square root of negative number")
            return math.sqrt(operand_val)
        elif self.operator == "abs":
            return abs(operand_val)
        else:
            raise ValueError(f"Unsupported unary operator: {self.operator}")

    def to_string(self) -> str:
        """Get string representation of the unary operation.

        Returns:
            str: String representation with appropriate notation
        """

        operand_str = self.operand.to_string()

        if isinstance(self.operand, BinaryOperation):
            operand_str = f"({operand_str})"

        if self.operator == "-":
            return f"-{operand_str}"
        elif self.operator == "sqrt":
            return f"sqrt({operand_str})"
        elif self.operator == "abs":
            return f"abs({operand_str})"
        else:
            return f"{self.operator}({operand_str})"

    def get_complexity(self) -> int:
        """Get the complexity of the unary operation.

        Returns:
            int: 1 plus the complexity of the operand
        """
        return 1 + self.operand.get_complexity()


# =============================================================================
# Utility Functions and Demonstrations
# =============================================================================


def create_sample_file_system() -> Directory:
    """Create a sample file system structure for demonstration.

    Returns:
        Directory: Root directory with sample files and subdirectories
    """

    # Create root directory
    root = Directory("MyProject")

    # Add some files to root
    root.add(File("README.md", 2048, "text"))
    root.add(File("LICENSE", 1024, "text"))
    root.add(File("requirements.txt", 512, "text"))

    # Create source code directory
    src = Directory("src")
    src.add(File("main.py", 4096, "text"))
    src.add(File("utils.py", 2048, "text"))
    src.add(File("config.json", 1024, "text"))

    # Create subdirectory in src
    models = Directory("models")
    models.add(File("user.py", 3072, "text"))
    models.add(File("product.py", 2560, "text"))
    src.add(models)

    root.add(src)

    # Create documentation directory
    docs = Directory("docs")
    docs.add(File("api.md", 8192, "text"))
    docs.add(File("tutorial.md", 6144, "text"))
    docs.add(File("diagram.png", 204800, "image"))
    root.add(docs)

    # Create test directory
    tests = Directory("tests")
    tests.add(File("test_main.py", 3072, "text"))
    tests.add(File("test_utils.py", 2048, "text"))
    root.add(tests)

    return root


def create_sample_organization() -> Department:
    """Create a sample organization structure for demonstration.

    Returns:
        Department: Root department with employees and subdepartments
    """

    # Create root company
    company = Department("TechCorp", "Company", 5000000.0)

    # Engineering Department
    engineering = Department("Engineering", "Department", 2000000.0)

    # Frontend Team
    frontend = Department("Frontend Team", "Team", 600000.0)
    frontend.add_report(
        Employee(
            "Alice Johnson",
            "Senior Frontend Developer",
            120000.0,
            "Engineering",
            ["React", "JavaScript", "CSS"],
        )
    )
    frontend.add_report(
        Employee(
            "Bob Smith",
            "Frontend Developer",
            95000.0,
            "Engineering",
            ["Vue.js", "HTML", "SASS"],
        )
    )

    # Backend Team
    backend = Department("Backend Team", "Team", 700000.0)
    backend.add_report(
        Employee(
            "Carol Davis",
            "Senior Backend Developer",
            125000.0,
            "Engineering",
            ["Python", "Django", "PostgreSQL"],
        )
    )
    backend.add_report(
        Employee(
            "David Wilson",
            "Backend Developer",
            100000.0,
            "Engineering",
            ["Node.js", "MongoDB", "Express"],
        )
    )
    backend.add_report(
        Employee(
            "Eve Brown",
            "DevOps Engineer",
            110000.0,
            "Engineering",
            ["Docker", "AWS", "Kubernetes"],
        )
    )

    engineering.add_report(frontend)
    engineering.add_report(backend)
    engineering.add_report(
        Employee(
            "Frank Miller",
            "Engineering Manager",
            150000.0,
            "Engineering",
            ["Leadership", "Architecture"],
        )
    )

    # Sales Department
    sales = Department("Sales", "Department", 1200000.0)
    sales.add_report(
        Employee(
            "Grace Taylor",
            "Sales Manager",
            130000.0,
            "Sales",
            ["B2B Sales", "CRM", "Negotiation"],
        )
    )
    sales.add_report(
        Employee(
            "Henry Clark",
            "Sales Representative",
            80000.0,
            "Sales",
            ["Lead Generation", "Customer Relations"],
        )
    )
    sales.add_report(
        Employee(
            "Ivy Anderson",
            "Sales Representative",
            75000.0,
            "Sales",
            ["Product Demos", "Market Research"],
        )
    )

    company.add_report(engineering)
    company.add_report(sales)
    company.add_report(
        Employee(
            "Jack Thompson", "CEO", 200000.0, "Executive", ["Strategy", "Leadership"]
        )
    )

    return company


def create_sample_ui() -> Panel:
    """Create a sample UI structure for demonstration.

    Returns:
        Panel: Root panel with various UI components
    """

    # Create main window
    main_window = Panel("MainWindow", 0, 0, 800, 600)

    # Create header panel
    header = Panel("Header", 0, 0, 800, 80)
    header.add_child(Label("Title", "My Application", 20, 20, 200, 30))
    header.add_child(Button("CloseButton", "X", 750, 20, 30, 30))
    main_window.add_child(header)

    # Create content panel
    content = Panel("Content", 0, 80, 800, 460)

    # Create left sidebar
    sidebar = Panel("Sidebar", 10, 10, 200, 440)
    sidebar.add_child(Button("HomeButton", "Home", 10, 10, 180, 40))
    sidebar.add_child(Button("SettingsButton", "Settings", 10, 60, 180, 40))
    sidebar.add_child(Button("AboutButton", "About", 10, 110, 180, 40))
    content.add_child(sidebar)

    # Create main content area
    main_content = Panel("MainContent", 220, 10, 570, 440)
    main_content.add_child(
        Label("WelcomeLabel", "Welcome to My Application!", 20, 20, 400, 30)
    )
    main_content.add_child(
        Label("DescriptionLabel", "This is a sample UI structure.", 20, 60, 400, 20)
    )
    main_content.add_child(Button("ActionButton", "Click Me", 20, 100, 120, 40))
    content.add_child(main_content)

    main_window.add_child(content)

    # Create footer
    footer = Panel("Footer", 0, 540, 800, 60)
    footer.add_child(Label("StatusLabel", "Ready", 20, 20, 100, 20))
    footer.add_child(Label("VersionLabel", "v1.0.0", 700, 20, 80, 20))
    main_window.add_child(footer)

    return main_window


def create_sample_math_expression() -> MathExpression:
    """Create a sample mathematical expression tree for demonstration.

    Returns:
        MathExpression: Complex mathematical expression
    """

    # Create expression: ((3 + 4) * 2) - sqrt(16) / 2
    # This demonstrates nested operations and different operator types

    # Sub-expression: (3 + 4)
    addition = BinaryOperation(Number(3), "+", Number(4))

    # Sub-expression: ((3 + 4) * 2)
    multiplication = BinaryOperation(addition, "*", Number(2))

    # Sub-expression: sqrt(16)
    sqrt_op = UnaryOperation("sqrt", Number(16))

    # Sub-expression: sqrt(16) / 2
    division = BinaryOperation(sqrt_op, "/", Number(2))

    # Final expression: ((3 + 4) * 2) - sqrt(16) / 2
    final_expression = BinaryOperation(multiplication, "-", division)

    return final_expression


# =============================================================================
# Demonstration Functions
# =============================================================================


def demo_file_system():
    """Demonstrate the file system composite pattern."""

    print("=" * 70)
    print("FILE SYSTEM COMPOSITE PATTERN DEMO")
    print("=" * 70)

    # Create and display file system
    root = create_sample_file_system()
    print("📁 Complete File System Structure:")
    print(root.display())

    print("\n📊 File System Statistics:")
    print(f"   Total size: {root.get_size() / 1024:.1f} KB")
    print(f"   Total files: {root.get_file_count()}")
    print(f"   Total directories: {root.get_directory_count() + 1}")  # +1 for root

    # Demonstrate search functionality
    print("\n🔍 Search Results:")
    found = root.find("models")
    if found:
        print(f"   Found: {found.get_path()} ({type(found).__name__})")

    # Show individual component operations
    print("\n🔧 Individual Operations:")
    src_dir = root.find("src")
    if src_dir:
        print(f"   'src' directory size: {src_dir.get_size() / 1024:.1f} KB")
        print(f"   'src' directory files: {src_dir.get_file_count()}")


def demo_organization():
    """Demonstrate the organization composite pattern."""
    print("\n" + "=" * 70)
    print("ORGANIZATION COMPOSITE PATTERN DEMO")
    print("=" * 70)

    # Create and display organization
    company = create_sample_organization()
    print("🏢 Organization Hierarchy:")
    print(company.display_hierarchy())

    print("\n📊 Organization Statistics:")
    print(f"   Total employees: {company.get_headcount()}")
    print(f"   Total salary cost: ${company.get_salary_cost():,.0f}")
    print(f"   Budget utilization: {company.get_budget_utilization():.1f}%")

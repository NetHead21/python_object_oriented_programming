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

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

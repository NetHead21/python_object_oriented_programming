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

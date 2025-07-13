"""
Strategy Pattern Implementation - Object-Oriented Design Pattern

This module demonstrates the Strategy design pattern using sorting algorithms as an example.
The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them
interchangeable. Strategy lets the algorithm vary independently from clients that use it.

Key Components:
--------------
1. Strategy (SortStrategy): Defines the interface common to all concrete strategies
2. ConcreteStrategy (BubbleSort, QuickSort): Implements the algorithm using the Strategy interface
3. Context: Uses a Strategy to perform its work

Benefits of Strategy Pattern:
----------------------------
• Runtime algorithm selection and switching
• Open/Closed Principle: Open for extension, closed for modification
• Eliminates conditional statements for algorithm selection
• Promotes code reusability and testability
• Separates concerns: algorithm implementation vs. usage

Use Cases:
----------
• Payment processing systems (different payment methods)
• Data compression algorithms
• Image/video encoding strategies
• Authentication mechanisms
• Pricing strategies in e-commerce

Author: Python OOP Tutorial
Date: July 2025
Python Version: 3.13+
Design Pattern: Strategy Pattern
"""

from abc import ABC, abstractmethod
import random


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        pass

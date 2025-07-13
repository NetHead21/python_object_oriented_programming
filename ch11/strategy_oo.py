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
    """
    Abstract base class for sorting strategies.

    This class defines the Strategy interface that all concrete sorting
    strategies must implement. It ensures that all sorting algorithms
    have a consistent interface for the Context to use.

    The Strategy pattern allows the Context to work with different
    algorithms without knowing their specific implementations.
    """

    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        """
        Concrete strategy implementing the Bubble Sort algorithm.

        Bubble Sort is a simple comparison-based sorting algorithm that repeatedly
        steps through the list, compares adjacent elements and swaps them if they
        are in the wrong order. The pass through the list is repeated until the
        list is sorted.

        Time Complexity:
            - Best Case: O(n) when the list is already sorted
            - Average Case: O(n²)
            - Worst Case: O(n²) when the list is reverse sorted

        Space Complexity: O(1) - sorts in-place

        Characteristics:
            - Stable: Equal elements maintain their relative order
            - In-place: Requires only O(1) additional memory
            - Simple: Easy to understand and implement
            - Inefficient: Poor performance on large datasets

        Best Used For:
            - Educational purposes
            - Small datasets (< 50 elements)
            - Nearly sorted data
            - When simplicity is more important than efficiency
        """

        pass


class BubbleSort(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        # Create a copy to avoid modifying the original list
        data = data.copy()
        n = len(data)

        # Traverse through all array elements
        for i in range(n):
            # Last i elements are already in place
            for j in range(0, n - i - 1):
                # Traverse the array from 0 to n-i-1
                # Swap if the element found is greater than the next element
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data

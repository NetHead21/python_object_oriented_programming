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
        """
        Sort data using the Bubble Sort algorithm.

        The algorithm works by repeatedly comparing adjacent elements
        and swapping them if they are in the wrong order. This process
        continues until no more swaps are needed.

        Args:
            data (list[int]): List of integers to sort

        Returns:
            list[int]: A new sorted list in ascending order

        Example:
            >>> bubble_sort = BubbleSort()
            >>> bubble_sort.sort([64, 34, 25, 12, 22, 11, 90])
            [11, 12, 22, 25, 34, 64, 90]
        """

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


class QuickSort(SortStrategy):
    """
    Concrete strategy implementing the QuickSort algorithm.

    QuickSort is a highly efficient divide-and-conquer sorting algorithm that
    works by selecting a 'pivot' element and partitioning the array around it,
    then recursively sorting the sub-arrays.

    Time Complexity:
        - Best Case: O(n log n) when pivot divides array evenly
        - Average Case: O(n log n)
        - Worst Case: O(n²) when pivot is always the smallest/largest element

    Space Complexity: O(log n) due to recursion stack

    Characteristics:
        - Not stable: Equal elements may not maintain relative order
        - In-place: Can be implemented to use O(log n) extra space
        - Efficient: Generally faster than other O(n log n) algorithms
        - Divide-and-conquer: Breaks problem into smaller subproblems

    Best Used For:
        - Large datasets
        - General-purpose sorting
        - When average-case performance is important
        - Systems where cache performance matters
    """

    def sort(self, data: list[int]) -> list[int]:
        """
        Sort data using the QuickSort algorithm.

        This implementation uses the middle element as the pivot and
        creates three partitions: elements less than pivot, equal to pivot,
        and greater than pivot. The less than and greater than partitions
        are recursively sorted.

        Args:
            data (list[int]): List of integers to sort

        Returns:
            list[int]: A new sorted list in ascending order

        Example:
            >>> quick_sort = QuickSort()
            >>> quick_sort.sort([64, 34, 25, 12, 22, 11, 90])
            [11, 12, 22, 25, 34, 64, 90]

        Note:
            This implementation creates new lists for partitions, making it
            easier to understand but using more memory than an in-place version.
        """

        # Base case: arrays with 0 or 1 element are already sorted
        if len(data) <= 1:
            return data

        # Choose the middle element as the pivot
        pivot = data[len(data) // 2]

        # Partition the array into three parts
        left = [x for x in data if x < pivot]  # Elements less than pivot
        middle = [x for x in data if x == pivot]  # Elements equal to pivot
        right = [x for x in data if x > pivot]  # Elements greater than pivot

        # Recursively sort the left and right partitions and combine
        return self.sort(left) + middle + self.sort(right)


class Context:
    """
    Context class that uses a sorting strategy to perform data processing.

    The Context maintains a reference to a Strategy object and delegates
    the sorting work to it. This class demonstrates how the Strategy pattern
    allows for runtime selection and switching of algorithms.

    The Context also performs additional data processing (multiplication and
    random number addition) before sorting, showing how the Strategy pattern
    can be part of a larger processing pipeline.

    Attributes:
        _strategy (SortStrategy): The current sorting strategy being used
    """

    def __init__(self, strategy: SortStrategy):
        """
        Initialize the Context with a sorting strategy.

        Args:
            strategy (SortStrategy): The initial sorting strategy to use

        Example:
            >>> context = Context(BubbleSort())
            >>> context = Context(QuickSort())
        """

        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        """
        Change the sorting strategy at runtime.

        This method demonstrates the flexibility of the Strategy pattern -
        the algorithm can be changed without modifying the Context's code.

        Args:
            strategy (SortStrategy): The new sorting strategy to use

        Example:
            >>> context = Context(BubbleSort())
            >>> context.set_strategy(QuickSort())  # Switch to QuickSort
        """

        self._strategy = strategy

    def execute(self, data: list[int]) -> list[int]:
        """
        Execute the complete data processing pipeline.

        This method performs the following operations:
        1. Multiply each element by 2
        2. Add a random number (0-10) to each element
        3. Sort the processed data using the current strategy

        Args:
            data (list[int]): Original list of integers to process

        Returns:
            list[int]: Processed and sorted list of integers

        Example:
            >>> context = Context(BubbleSort())
            >>> result = context.execute([3, 1, 4])
            >>> # Result will be sorted list where each original element
            >>> # was multiplied by 2 and had 0-10 added to it

        Note:
            Due to the random number addition, the exact output will vary
            between runs, but the data will always be sorted according
            to the current strategy.
        """

        # Step 1: Multiply each element by 2
        data = [x * 2 for x in data]

        # Step 2: Add a random number (0-10) to each element
        data = [x + random.randint(0, 10) for x in data]

        # Step 3: Sort using the current strategy
        return self._strategy.sort(data)

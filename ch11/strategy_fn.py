"""
Strategy Pattern Implementation - Functional Programming Approach

This module demonstrates the Strategy design pattern using a functional programming
approach with sorting algorithms as an example. Unlike the object-oriented version,
this implementation uses functions as strategies rather than classes.

Functional Strategy Pattern:
---------------------------
In functional programming, strategies are simply functions that share the same
signature. This approach is more lightweight and leverages Python's first-class
function support to achieve the same design goals as the classic Strategy pattern.

Key Components:
--------------
1. Strategy Functions: Individual functions implementing different algorithms
2. Strategy Type: Type alias defining the function signature
3. Context Function: Function that accepts and uses strategy functions

Benefits of Functional Approach:
-------------------------------
• Simpler implementation without class boilerplate
• Leverages Python's first-class function support
• More concise and readable code
• Easy to add new strategies as simple functions
• Natural fit for functional programming paradigms
• Reduced memory overhead (no object instantiation)

Comparison with OOP Strategy:
----------------------------
• Functional: Functions as strategies, passed as parameters
• OOP: Classes as strategies, injected as dependencies
• Functional: Less ceremony, more direct
• OOP: More structure, better for complex strategies with state

Use Cases for Functional Strategy:
---------------------------------
• Stateless algorithms and operations
• Mathematical computations with different methods
• Data transformation pipelines
• Validation strategies
• Simple business rules without complex state

Author: Python OOP Tutorial
Date: July 2025
Python Version: 3.13+
Design Pattern: Strategy Pattern (Functional Implementation)
"""

import random
from typing import Callable


def bubble_sort(data: list[int]) -> list[int]:
    """
    Implement the Bubble Sort algorithm as a strategy function.

    Bubble Sort is a simple comparison-based sorting algorithm that repeatedly
    steps through the list, compares adjacent elements and swaps them if they
    are in the wrong order. The pass through the list is repeated until the
    list is sorted.

    Algorithm Characteristics:
    -------------------------
    Time Complexity:
        - Best Case: O(n) when the list is already sorted
        - Average Case: O(n²)
        - Worst Case: O(n²) when the list is reverse sorted

    Space Complexity: O(1) - sorts in-place (after copying input)

    Properties:
        - Stable: Equal elements maintain their relative order
        - In-place: Requires only O(1) additional memory after copy
        - Adaptive: Performance improves on partially sorted data
        - Simple: Easy to understand and implement

    Best Used For:
        - Educational purposes and algorithm learning
        - Small datasets (< 50 elements)
        - Nearly sorted data where simplicity matters
        - Situations where code clarity is more important than efficiency

    Args:
        data (list[int]): List of integers to sort. The original list
                         is not modified due to copying.

    Returns:
        list[int]: A new sorted list in ascending order.

    Example:
        >>> bubble_sort([64, 34, 25, 12, 22, 11, 90])
        [11, 12, 22, 25, 34, 64, 90]

        >>> bubble_sort([5, 1, 4, 2, 8])
        [1, 2, 4, 5, 8]

        >>> bubble_sort([1])  # Single element
        [1]

        >>> bubble_sort([])   # Empty list
        []

    Note:
        This implementation creates a copy of the input list to avoid
        modifying the original data, following functional programming
        principles of immutability.
    """
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


def quick_sort(data: list[int]) -> list[int]:
    """
    Implement the Quick Sort algorithm as a strategy function.

    Quick Sort is a highly efficient divide-and-conquer sorting algorithm
    that works by selecting a 'pivot' element and partitioning the array
    around the pivot, then recursively sorting the sub-arrays.

    Algorithm Characteristics:
    -------------------------
    Time Complexity:
        - Best Case: O(n log n) with good pivot selection
        - Average Case: O(n log n)
        - Worst Case: O(n²) when pivot is always the smallest/largest

    Space Complexity: O(log n) due to recursion stack in average case,
                     O(n) in worst case

    Properties:
        - Unstable: Equal elements may not maintain relative order
        - In-place: Can be implemented in-place (this version creates new lists)
        - Divide-and-conquer: Breaks problem into smaller subproblems
        - Cache-efficient: Good locality of reference

    Pivot Selection Strategy:
        This implementation uses the middle element as pivot, which
        provides good performance for many real-world datasets and
        avoids worst-case behavior on already-sorted data.

    Best Used For:
        - Large datasets (> 100 elements)
        - General-purpose sorting where performance matters
        - Datasets with random or partially sorted elements
        - When average O(n log n) performance is acceptable

    Args:
        data (list[int]): List of integers to sort. Original list is preserved.

    Returns:
        list[int]: A new sorted list in ascending order.

    Example:
        >>> quick_sort([64, 34, 25, 12, 22, 11, 90])
        [11, 12, 22, 25, 34, 64, 90]

        >>> quick_sort([3, 6, 8, 10, 1, 2, 1])
        [1, 1, 2, 3, 6, 8, 10]

        >>> quick_sort([5])  # Single element
        [5]

        >>> quick_sort([])   # Empty list
        []

    Algorithm Steps:
        1. Choose middle element as pivot
        2. Partition: elements < pivot, = pivot, > pivot
        3. Recursively sort left and right partitions
        4. Combine: left + middle + right

    Note:
        This functional implementation creates new lists rather than
        sorting in-place, following functional programming principles
        but using more memory than an in-place version.
    """
    if len(data) <= 1:
        return data

    # Choose the middle element as the pivot
    pivot = data[len(data) // 2]

    # Partition the array into three parts
    left = [x for x in data if x < pivot]  # Elements less than pivot
    middle = [x for x in data if x == pivot]  # Elements equal to pivot
    right = [x for x in data if x > pivot]  # Elements greater than pivot

    # Recursively sort the left and right partitions and combine
    return quick_sort(left) + middle + quick_sort(right)


# Type alias for sorting strategy functions
SortFn = Callable[[list[int]], list[int]]


"""
Type alias for sorting strategy functions.

This type alias defines the signature that all sorting strategy functions
must follow in this functional implementation of the Strategy pattern.

Function Signature:
    - Input: list[int] - A list of integers to sort
    - Output: list[int] - A new sorted list in ascending order

Benefits of Type Alias:
    • Improves code readability and self-documentation
    • Enables better type checking and IDE support
    • Makes function signatures more maintainable
    • Clearly communicates the strategy contract

Usage:
    Any function that matches this signature can be used as a sorting
    strategy in the context function. This allows for easy extension
    of the system with new sorting algorithms.

Example:
    def my_custom_sort(data: list[int]) -> list[int]:
        # Custom sorting implementation
        return sorted(data)
    
    # my_custom_sort automatically conforms to SortFn type
    result = context(my_custom_sort, [3, 1, 4, 1, 5])
"""

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

"""
operator.itemgetter Comprehensive Tutorial and Examples

This module demonstrates the powerful capabilities of Python's `operator.itemgetter` function,
which provides an efficient way to extract items from sequences, mappings, and other subscriptable objects.

Overview:
---------
The `itemgetter` function returns a callable object that fetches the given item(s)
from its operand using the subscription operator []. It's particularly useful for:
- Extracting specific elements from lists, tuples, and sequences
- Accessing dictionary values by key
- Sorting collections by specific indices or keys
- Data extraction and transformation operations
- Functional programming patterns

Key Features:
------------
✨ Single and multiple item extraction
✨ Works with any subscriptable object (lists, tuples, dicts, etc.)
✨ Performance optimized for large datasets
✨ Clean, readable code for data operations
✨ Seamless integration with built-in functions (sorted, max, min, etc.)

Performance Benefits:
--------------------
- Faster than lambda functions for simple item access
- Memory efficient for large datasets
- Optimized C implementation in CPython
- Reduces function call overhead

Author: Python OOP Tutorial
Date: July 2025
Python Version: 3.13+
"""

from operator import itemgetter
from itertools import groupby
from collections import defaultdict
import time


# =============================================================================
# Example 1: Basic Single Item Access
# =============================================================================
"""
Basic Single Item Access with itemgetter

This section demonstrates how to use itemgetter to extract single items
from various types of sequences including lists, tuples, and strings.

Key Learning Points:
• itemgetter(n) creates a callable that returns obj[n]
• Works with any subscriptable object
• Same getter can be reused on different data types
• Efficient for repeated access to the same index

Use Cases:
• Extracting specific columns from data rows
• Getting consistent field positions from records
• Performance-critical index access in loops
"""

print("=" * 60)
print("Example 1: Basic Single Item Access")
print("=" * 60)

# Create some sample data
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
numbers = [10, 25, 30, 45, 50]
coordinates = [(1, 2), (3, 4), (5, 6), (7, 8)]

# Get item at index 2
get_index_2 = itemgetter(2)

print(f"Original fruits: {fruits}")
print(f"Item at index 2: {get_index_2(fruits)}")  # cherry

print(f"Original numbers: {numbers}")
print(f"Item at index 2: {get_index_2(numbers)}")  # 30

print(f"Original coordinates: {coordinates}")
print(f"Item at index 2: {get_index_2(coordinates)}")  # (5, 6)

# Works with strings too
text = "Hello World"
print(f"Character at index 2 in '{text}': {get_index_2(text)}")  # l

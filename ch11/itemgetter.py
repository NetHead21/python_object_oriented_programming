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


# =============================================================================
# Example 2: Multiple Item Access
# =============================================================================
"""
Multiple Item Access with itemgetter

This section shows how itemgetter can extract multiple items simultaneously,
returning them as a tuple. This is particularly useful for data transformation
and extraction operations where you need several fields at once.

Key Learning Points:
• itemgetter(a, b, c) returns (obj[a], obj[b], obj[c])
• Always returns a tuple for multiple items
• Maintains order of specified indices
• More efficient than multiple single accesses

Use Cases:
• Extracting multiple columns from database-like structures
• Tuple unpacking for specific fields
• Data transformation pipelines
• Creating derived data structures
"""

print("\n" + "=" * 60)
print("Example 2: Multiple Item Access")
print("=" * 60)

# Extract multiple items at once
get_multiple = itemgetter(0, 2, 4)

print(f"Original fruits: {fruits}")
print(
    f"Items at indices 0, 2, 4: {get_multiple(fruits)}"
)  # ('apple', 'cherry', 'elderberry')

print(f"Original numbers: {numbers}")
print(f"Items at indices 0, 2, 4: {get_multiple(numbers)}")  # (10, 30, 50)

# Extract from nested tuples
get_first_coord = itemgetter(0)
get_second_coord = itemgetter(1)

print(f"First coordinates: {[get_first_coord(coord) for coord in coordinates]}")
print(f"Second coordinates: {[get_second_coord(coord) for coord in coordinates]}")


# =============================================================================
# Example 3: Dictionary Operations
# =============================================================================
"""
Dictionary Operations with itemgetter

This section demonstrates how itemgetter works seamlessly with dictionaries
and other mapping types. itemgetter treats dictionary keys the same way
it treats sequence indices.

Key Learning Points:
• itemgetter('key') returns obj['key'] for dictionaries
• Can extract multiple keys simultaneously
• Works with any mapping type that supports [] operator
• Perfect for processing structured data records

Use Cases:
• Extracting fields from JSON-like data structures
• Processing database query results
• Configuration data access
• API response data extraction
"""

print("\n" + "=" * 60)
print("Example 3: Dictionary Operations")
print("=" * 60)

# Sample dictionaries
person1 = {"name": "Alice", "age": 30, "city": "New York", "salary": 75000}
person2 = {"name": "Bob", "age": 25, "city": "London", "salary": 65000}
person3 = {"name": "Charlie", "age": 35, "city": "Tokyo", "salary": 80000}

people = [person1, person2, person3]

# Extract single values
get_name = itemgetter("name")
get_age = itemgetter("age")
get_salary = itemgetter("salary")

print("People data:")
for person in people:
    print(
        f"  {get_name(person)}: {get_age(person)} years old, salary: ${get_salary(person)}"
    )

# Extract multiple values
get_name_and_city = itemgetter("name", "city")

print("\nName and city combinations:")
for person in people:
    name, city = get_name_and_city(person)
    print(f"  {name} lives in {city}")


# =============================================================================
# Example 4: Sorting with itemgetter
# =============================================================================
"""
Sorting Operations with itemgetter

This section shows one of the most powerful use cases for itemgetter:
sorting collections by specific attributes or indices. itemgetter provides
a clean, readable alternative to lambda functions for sorting operations.

Key Learning Points:
• itemgetter integrates seamlessly with sorted(), list.sort(), etc.
• Can sort by single or multiple criteria
• More readable than lambda equivalents
• Better performance than lambda for simple operations
• Supports reverse sorting and complex sorting strategies

Use Cases:
• Sorting data tables by column
• Multi-level sorting (primary, secondary keys)
• Performance-critical sorting operations
• Database-style ordering of results
"""

print("\n" + "=" * 60)
print("Example 4: Sorting with itemgetter")
print("=" * 60)

# Sample data for sorting
students = [
    ("Alice", 85, "Math"),
    ("Bob", 92, "Science"),
    ("Charlie", 78, "Math"),
    ("Diana", 95, "Science"),
    ("Eve", 88, "Art"),
]

print("Original student data (name, grade, subject):")
for student in students:
    print(f"  {student}")

# Sort by grade (index 1)
sorted_by_grade = sorted(students, key=itemgetter(1))
print("\nSorted by grade:")
for student in sorted_by_grade:
    print(f"  {student}")

# Sort by subject (index 2), then by grade (index 1)
sorted_by_subject_grade = sorted(students, key=itemgetter(2, 1))
print("\nSorted by subject, then by grade:")
for student in sorted_by_subject_grade:
    print(f"  {student}")

# Dictionary sorting
people_dict = [
    {"name": "Alice", "age": 30, "salary": 75000},
    {"name": "Bob", "age": 25, "salary": 65000},
    {"name": "Charlie", "age": 35, "salary": 80000},
    {"name": "Diana", "age": 28, "salary": 70000},
]

# Sort by salary (descending)
sorted_by_salary = sorted(people_dict, key=itemgetter("salary"), reverse=True)
print("\nSorted by salary (highest first):")
for person in sorted_by_salary:
    print(f"  {person['name']}: ${person['salary']}")

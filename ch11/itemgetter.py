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


# =============================================================================
# Example 5: Data Analysis and Grouping
# =============================================================================
"""
Data Analysis and Grouping with itemgetter

This section demonstrates how itemgetter works excellently with itertools.groupby
for data analysis tasks. The combination provides powerful data processing
capabilities for analytical workflows.

Key Learning Points:
• itemgetter + groupby creates powerful analysis pipelines
• Efficient grouping by specific fields or indices
• Works well with aggregation functions (sum, max, min, etc.)
• Maintains data relationships during transformations

Use Cases:
• Sales data analysis by period/category
• Log file analysis and aggregation
• Survey response grouping and analysis
• Financial data processing by time periods
"""

print("\n" + "=" * 60)
print("Example 5: Data Analysis and Grouping")
print("=" * 60)

# Sales data
sales_data = [
    ("Q1", "Electronics", 50000),
    ("Q1", "Clothing", 30000),
    ("Q1", "Books", 15000),
    ("Q2", "Electronics", 55000),
    ("Q2", "Clothing", 32000),
    ("Q2", "Books", 18000),
    ("Q3", "Electronics", 60000),
    ("Q3", "Clothing", 35000),
    ("Q3", "Books", 20000),
]

# Group by quarter
get_quarter = itemgetter(0)
get_category = itemgetter(1)
get_sales = itemgetter(2)

# Sort by quarter first
sales_by_quarter = sorted(sales_data, key=get_quarter)

print("Sales by quarter:")
for quarter, group in groupby(sales_by_quarter, key=get_quarter):
    total_sales = sum(get_sales(item) for item in group)
    print(f"  {quarter}: ${total_sales:,}")

# Find best performing category
sales_by_category = sorted(sales_data, key=get_category)
print("\nSales by category:")
for category, group in groupby(sales_by_category, key=get_category):
    group_list = list(group)
    total_sales = sum(get_sales(item) for item in group_list)
    print(f"  {category}: ${total_sales:,}")


# =============================================================================
# Example 6: Complex Data Structures
# =============================================================================
"""
Complex Data Structures with itemgetter

This section shows how itemgetter handles complex nested data structures
like lists of dictionaries, hierarchical data, and mixed-type collections.
itemgetter excels at extracting data from real-world complex structures.

Key Learning Points:
• itemgetter works with any subscriptable object
• Can handle deeply nested structures
• Maintains type safety and error handling
• Excellent for processing API responses and JSON data

Use Cases:
• Processing nested JSON/API responses
• Extracting data from database query results
• Configuration file processing
• Complex data transformation pipelines
"""

print("\n" + "=" * 60)
print("Example 6: Complex Data Structures")
print("=" * 60)

# Nested data structure
company_data = [
    {
        "company": "TechCorp",
        "employees": [
            {"name": "Alice", "department": "Engineering", "salary": 95000},
            {"name": "Bob", "department": "Marketing", "salary": 70000},
        ],
        "revenue": 1000000,
    },
    {
        "company": "DataInc",
        "employees": [
            {"name": "Charlie", "department": "Engineering", "salary": 90000},
            {"name": "Diana", "department": "Sales", "salary": 75000},
        ],
        "revenue": 800000,
    },
]

# Extract company information
get_company_name = itemgetter("company")
get_employees = itemgetter("employees")
get_revenue = itemgetter("revenue")

print("Company analysis:")
for company in company_data:
    name = get_company_name(company)
    employees = get_employees(company)
    revenue = get_revenue(company)

    print(f"\n{name}:")
    print(f"  Revenue: ${revenue:,}")
    print("  Employees:")

    # Extract employee data
    get_emp_name = itemgetter("name")
    get_emp_dept = itemgetter("department")
    get_emp_salary = itemgetter("salary")

    for emp in employees:
        print(
            f"    {get_emp_name(emp)} ({get_emp_dept(emp)}): ${get_emp_salary(emp):,}"
        )


# =============================================================================
# Example 7: Performance Comparison
# =============================================================================
"""
Performance Analysis of itemgetter

This section provides empirical performance comparison between itemgetter
and alternative approaches like direct indexing and lambda functions.
Understanding performance characteristics helps in choosing the right tool.

Key Learning Points:
• itemgetter performance vs. alternatives
• When performance differences matter
• Memory efficiency considerations
• Scale-dependent performance characteristics

Use Cases:
• Performance-critical data processing
• Large dataset operations
• Benchmarking and optimization decisions
• Understanding trade-offs in functional programming
"""

print("\n" + "=" * 60)
print("Example 7: Performance Comparison")
print("=" * 60)

# Create large dataset
large_dataset = [(i, i * 2, i * 3) for i in range(100000)]

# Method 1: Using itemgetter
get_second_item = itemgetter(1)
start = time.time()
result1 = [get_second_item(item) for item in large_dataset]
time1 = time.time() - start

# Method 2: Direct indexing
start = time.time()
result2 = [item[1] for item in large_dataset]
time2 = time.time() - start

# Method 3: Lambda function
start = time.time()
result3 = list(map(lambda x: x[1], large_dataset))
time3 = time.time() - start

print("Performance comparison (100,000 items):")
print(f"  itemgetter: {time1:.4f}s")
print(f"  Direct indexing: {time2:.4f}s")
print(f"  Lambda function: {time3:.4f}s")

# Verify results are the same
print(f"Results identical: {result1 == result2 == result3}")

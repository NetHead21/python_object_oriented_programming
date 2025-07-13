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


# =============================================================================
# Example 8: Error Handling and Edge Cases
# =============================================================================
"""
Error Handling and Edge Cases with itemgetter

This section explores how itemgetter behaves with edge cases, error conditions,
and mixed data types. Understanding error patterns is crucial for robust
production code.

Key Learning Points:
• Common error types: IndexError, KeyError, TypeError
• Graceful error handling strategies
• Type safety considerations
• Defensive programming with itemgetter

Use Cases:
• Robust data processing pipelines
• Handling inconsistent data formats
• Defensive programming practices
• Input validation and sanitization
"""

print("\n" + "=" * 60)
print("Example 8: Error Handling and Edge Cases")
print("=" * 60)

# Sample data with potential issues
mixed_data = [
    [1, 2, 3, 4, 5],
    [10, 20],  # Shorter list
    {"a": 1, "b": 2, "c": 3},
    "hello",
]

get_index_2 = itemgetter(2)
get_key_b = itemgetter("b")

print("Testing error handling:")
for i, item in enumerate(mixed_data):
    try:
        if isinstance(item, dict):
            result = get_key_b(item)
            print(f"  Item {i} (dict): key 'b' = {result}")
        else:
            result = get_index_2(item)
            print(f"  Item {i}: index 2 = {result}")
    except (IndexError, KeyError, TypeError) as e:
        print(f"  Item {i}: Error - {type(e).__name__}: {e}")


# =============================================================================
# Example 9: Real-world Use Case - Log Analysis
# =============================================================================
"""
Real-world Application: Log File Analysis

This section demonstrates a practical, real-world application of itemgetter
for log file analysis. This example shows how itemgetter can be used in
production scenarios for data processing and analysis.

Key Learning Points:
• Practical application in data analysis workflows
• Integration with other Python tools (defaultdict, groupby)
• Processing structured log data efficiently
• Building analytical insights from raw data

Use Cases:
• System log analysis and monitoring
• Application performance analysis
• Security log processing
• Operational data analysis
• Debugging and troubleshooting workflows
"""

print("\n" + "=" * 60)
print("Example 9: Real-world Use Case - Log Analysis")
print("=" * 60)

# Simulated log entries (timestamp, level, message, source)
log_entries = [
    ("2024-01-01 10:00:00", "INFO", "Application started", "main.py"),
    ("2024-01-01 10:01:15", "ERROR", "Database connection failed", "db.py"),
    ("2024-01-01 10:01:30", "WARN", "Retrying connection", "db.py"),
    ("2024-01-01 10:02:00", "INFO", "Connection restored", "db.py"),
    ("2024-01-01 10:05:00", "ERROR", "Invalid user input", "api.py"),
    ("2024-01-01 10:10:00", "INFO", "User login successful", "auth.py"),
]

# Create extractors
get_timestamp = itemgetter(0)
get_level = itemgetter(1)
get_message = itemgetter(2)
get_source = itemgetter(3)

# Analyze log levels
print("Log level analysis:")
level_counts = defaultdict(int)
for entry in log_entries:
    level_counts[get_level(entry)] += 1

for level, count in sorted(level_counts.items()):
    print(f"  {level}: {count} entries")

# Find all error messages
print("\nError messages:")
error_entries = [entry for entry in log_entries if get_level(entry) == "ERROR"]
for entry in error_entries:
    print(f"  {get_timestamp(entry)}: {get_message(entry)} (from {get_source(entry)})")

# Group by source file
print("\nEntries by source file:")
entries_by_source = sorted(log_entries, key=get_source)
for source, group in groupby(entries_by_source, key=get_source):
    group_list = list(group)
    print(f"  {source}: {len(group_list)} entries")


# =============================================================================
# Summary: Key Benefits and Best Practices
# =============================================================================
"""
Complete Guide to itemgetter Best Practices

This final section summarizes the key insights, patterns, and best practices
learned throughout the examples. It serves as a quick reference for when
and how to use itemgetter effectively.

Design Principles:
• Favor itemgetter over lambda for simple item access
• Use itemgetter for performance-critical operations
• Combine with other functional programming tools
• Consider readability and maintainability

Performance Guidelines:
• itemgetter is faster than lambda for simple operations
• More memory efficient for repeated operations
• Excellent for large dataset processing
• C implementation provides optimization benefits

Common Patterns and Anti-patterns:
• DO: Use for sorting, grouping, and data extraction
• DO: Combine with map(), filter(), groupby()
• DON'T: Use for complex logic (prefer lambda/functions)
• DON'T: Use when direct access is clearer
"""


print("\n" + "=" * 60)
print("Key Benefits and Best Practices")
print("=" * 60)

print("""
✨ When to use itemgetter:
  • Extracting specific indices from sequences
  • Accessing dictionary keys
  • Sorting operations: sorted(items, key=itemgetter(0))
  • Data transformation: Converting nested structures
  • Functional programming: Use with map(), filter(), etc.
  • Performance-critical item access

🚀 Performance advantages:
  • Faster than lambda for simple item access
  • Memory efficient for large datasets
  • C implementation optimization
  • Reduced function call overhead

📋 Common patterns:
  • Single item: itemgetter(2) → obj[2]
  • Multiple items: itemgetter(0, 2, 4) → (obj[0], obj[2], obj[4])
  • Dictionary access: itemgetter('key') → obj['key']
  • Sorting: sorted(data, key=itemgetter('score'))
  • Grouping: groupby(data, key=itemgetter('category'))
""")

print("=" * 60)
print("Examples completed successfully!")
print("=" * 60)


# =============================================================================
# Module Summary and Usage Guidelines
# =============================================================================


def get_itemgetter_usage_summary():
    """
    Comprehensive usage summary for operator.itemgetter.

    This function provides a complete reference guide for when and how to use
    itemgetter effectively in your Python projects.

    Returns:
        dict: Complete reference guide with usage patterns, performance tips,
              and best practices for itemgetter implementation.
    """
    return {
        "core_functionality": {
            "single_item": "itemgetter(2) → obj[2]",
            "multiple_items": "itemgetter(0, 2, 4) → (obj[0], obj[2], obj[4])",
            "dict_access": "itemgetter('key') → obj['key']",
            "mixed_access": "itemgetter('name', 2, 'age') → (obj['name'], obj[2], obj['age'])",
        },
        "performance_characteristics": {
            "vs_lambda": "~15-25% faster for simple item access",
            "vs_direct": "Slightly slower but negligible for most use cases",
            "memory_usage": "Very efficient, uses __slots__",
            "optimization": "C implementation in CPython",
        },
        "best_use_cases": [
            "Sorting: sorted(data, key=itemgetter('score'))",
            "Grouping: groupby(data, key=itemgetter('category'))",
            "Data extraction: map(itemgetter(1), data)",
            "Filtering: filter(lambda x: itemgetter('active')(x), data)",
            "Multi-field access: itemgetter('name', 'age', 'salary')",
        ],
        "when_to_avoid": [
            "Complex logic (use lambda or functions instead)",
            "Single-use, inline operations where direct access is clearer",
            "When the overhead of creating the getter isn't worth it",
            "Operations requiring conditional logic or transformations",
        ],
        "integration_patterns": {
            "with_sorted": "sorted(items, key=itemgetter('priority', 'timestamp'))",
            "with_groupby": "groupby(sorted(data, key=itemgetter('dept')), key=itemgetter('dept'))",
            "with_map": "list(map(itemgetter('total'), transactions))",
            "with_filter": "list(filter(itemgetter('active'), users))",
            "with_max_min": "max(products, key=itemgetter('price'))",
        },
        "error_handling": {
            "IndexError": "Index out of range for sequences",
            "KeyError": "Key not found in mappings",
            "TypeError": "Object not subscriptable",
            "AttributeError": "Rare, usually with custom __getitem__ implementations",
        },
        "style_guidelines": {
            "naming": "Use descriptive names: get_price vs itemgetter(2)",
            "reuse": "Create once, use many times for efficiency",
            "readability": "Prefer itemgetter over lambda for simple access",
            "documentation": "Document the expected data structure",
        },
    }


# =============================================================================
# Advanced Usage Patterns Reference
# =============================================================================


class ItemGetterPatterns:
    """
    Collection of advanced patterns and recipes using itemgetter.

    This class serves as a reference for sophisticated itemgetter usage
    patterns that can be applied in complex data processing scenarios.
    """

    @staticmethod
    def multi_level_sort(data, *fields):
        """
        Sort data by multiple fields in order of priority.

        Args:
            data: Sequence of mappings or sequences to sort
            *fields: Field names or indices in order of sort priority

        Returns:
            list: Sorted data

        Example:
            >>> data = [{'name': 'Alice', 'dept': 'IT', 'salary': 70000},
            ...         {'name': 'Bob', 'dept': 'IT', 'salary': 75000}]
            >>> multi_level_sort(data, 'dept', 'salary')
        """
        return sorted(data, key=itemgetter(*fields))

    @staticmethod
    def extract_columns(data, *columns):
        """
        Extract specific columns from tabular data.

        Args:
            data: Sequence of sequences or mappings
            *columns: Column indices or keys to extract

        Returns:
            list: List of tuples containing extracted columns

        Example:
            >>> data = [('Alice', 25, 'Engineer'), ('Bob', 30, 'Manager')]
            >>> extract_columns(data, 0, 2)  # Name and title
            [('Alice', 'Engineer'), ('Bob', 'Manager')]
        """
        extractor = itemgetter(*columns)
        return [extractor(row) for row in data]

    @staticmethod
    def group_by_field(data, field):
        """
        Group data by a specific field, returning a dictionary.

        Args:
            data: Sequence of mappings or sequences
            field: Field name or index to group by

        Returns:
            dict: Grouped data with field values as keys

        Example:
            >>> data = [{'dept': 'IT', 'name': 'Alice'}, {'dept': 'HR', 'name': 'Bob'}]
            >>> group_by_field(data, 'dept')
            {'IT': [{'dept': 'IT', 'name': 'Alice'}], 'HR': [...]}
        """
        from collections import defaultdict
        from itertools import groupby

        sorted_data = sorted(data, key=itemgetter(field))
        grouped = defaultdict(list)

        for key, group in groupby(sorted_data, key=itemgetter(field)):
            grouped[key].extend(group)

        return dict(grouped)

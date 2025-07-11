"""
Python operator.attrgetter - Comprehensive Examples and Usage Guide
==================================================================

This module demonstrates the powerful capabilities of Python's `operator.attrgetter`
function through practical examples and real-world use cases.

Overview
--------
The `attrgetter` function from the `operator` module is a utility that creates
callable objects for extracting attributes from other objects. It's particularly
useful for functional programming, data processing, and when you need to pass
attribute access as a function to other functions like `sorted()`, `map()`, or
`groupby()`.

Key Features Demonstrated:
-------------------------
1. **Basic Attribute Access**: Extract single attributes from objects
2. **Multiple Attributes**: Get multiple attributes as tuples
3. **Nested Attributes**: Access deeply nested attributes using dot notation
4. **Sorting and Grouping**: Use with sorting algorithms and grouping operations
5. **Performance**: Compare performance with direct access and lambda functions
6. **Error Handling**: Safely handle missing attributes
7. **Real-world Applications**: Log analysis, data processing, and more

Examples Included:
-----------------
- Basic usage with Person objects
- Multiple attribute extraction
- Nested attribute access (Employee.address.city)
- Sorting products by price and rating
- Grouping students by subject and grade
- Complex nested structures (Company/Department/Employee)
- Error handling for missing attributes
- Performance benchmarks vs direct access and lambdas
- Real-world log analysis example

When to Use attrgetter:
----------------------
✅ Sorting by object attributes: `sorted(items, key=attrgetter('price'))`
✅ Extracting data for processing: Converting objects to tuples/lists
✅ Functional programming: Passing to `map()`, `filter()`, `groupby()`
✅ Performance-critical attribute access
✅ Clean syntax for nested attributes: `attrgetter('user.profile.name')`
✅ Grouping operations with `itertools.groupby()`

Performance Notes:
-----------------
- `attrgetter` is typically faster than lambda functions for simple attribute access
- Particularly efficient when used repeatedly (e.g., in sorting large datasets)
- Creates reusable callable objects that can be stored and passed around

Author: Assistant
Date: July 2025
Python Version: 3.13+
Dependencies: operator, itertools, collections, time
"""

from operator import attrgetter
from itertools import groupby
from collections import defaultdict
import time

"""
operator.attrgetter Comprehensive Tutorial and Examples

This module demonstrates the powerful capabilities of Python's `operator.attrgetter` function,
which provides an efficient and readable way to extract attributes from objects.

Overview:
---------
The `attrgetter` function returns a callable object that fetches the given attribute(s) 
from its operand. It's particularly useful for:
- Sorting collections of objects
- Data extraction and transformation
- Functional programming patterns
- Performance-critical attribute access
- Nested attribute navigation

Key Features:
------------
✨ Single and multiple attribute extraction
✨ Nested attribute access using dot notation
✨ Performance optimized for large datasets
✨ Clean, readable code for complex data operations
✨ Seamless integration with built-in functions (sorted, max, min, etc.)
✨ Error handling for missing attributes

Common Use Cases:
----------------
1. **Sorting**: Sort objects by one or more attributes
2. **Grouping**: Group objects by shared attributes
3. **Filtering**: Extract objects based on attribute values
4. **Data Processing**: Transform object collections to simple data types
5. **Analytics**: Aggregate and analyze object attributes

Performance Benefits:
--------------------
- Faster than lambda functions for simple attribute access
- Memory efficient for large datasets
- Optimized C implementation in CPython
- Reduces function call overhead

Examples Included:
-----------------
• Basic single and multiple attribute access
• Nested attribute navigation (obj.attr.subattr)
• Sorting collections by attributes
• Grouping and filtering operations
• Complex nested data structures
• Error handling and edge cases
• Performance comparisons
• Real-world data processing scenarios

Author: Python OOP Tutorial
Date: July 2025
Python Version: 3.13+
"""


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person('{self.name}', {self.age})"


# Create some people
people = [Person("Alice", 30), Person("Bob", 25), Person("Charlie", 35)]

# Create an attrgetter for the 'name' attribute
get_name = attrgetter("name")

# Use it to extract names
for person in people:
    print(get_name(person))
# Output:
# Alice
# Bob
# Charlie

# Extract all names at once
names = [get_name(person) for person in people]
print(names)  # ['Alice', 'Bob', 'Charlie']


# Example 2: Multiple Attributes

# Get multiple attributes at once
get_name_age = attrgetter("name", "age")

for person in people:
    print(get_name_age(person))
# Output:
# ('Alice', 30)
# ('Bob', 25)
# ('Charlie', 35)


# 🏗️ Nested Attribute Access
# Example 3: Dot Notation for Nested Attributes


class Address:
    def __init__(self, street, city, country):
        self.street = street
        self.city = city
        self.country = country


class Employee:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __repr__(self):
        return f"Employee('{self.name}')"


# Create employees with addresses
employees = [
    Employee("Alice", Address("123 Main St", "New York", "USA")),
    Employee("Bob", Address("456 Oak Ave", "London", "UK")),
    Employee("Charlie", Address("789 Pine Rd", "Tokyo", "Japan")),
]

# Access nested attributes using dot notation
get_city = attrgetter("address.city")
get_country = attrgetter("address.country")

for emp in employees:
    print(f"{emp.name} lives in {get_city(emp)}, {get_country(emp)}")
# Output:
# Alice lives in New York, USA
# Bob lives in London, UK
# Charlie lives in Tokyo, Japan

# Multiple nested attributes
get_address_info = attrgetter("name", "address.city", "address.country")
for emp in employees:
    name, city, country = get_address_info(emp)
    print(f"{name}: {city}, {country}")


# 📊 Practical Use Cases
# Example 4: Sorting with attrgetter


class Product:
    def __init__(self, name, price, rating):
        self.name = name
        self.price = price
        self.rating = rating

    def __repr__(self):
        return f"Product('{self.name}', ${self.price}, ⭐{self.rating})"


products = [
    Product("Laptop", 999.99, 4.5),
    Product("Mouse", 29.99, 4.2),
    Product("Keyboard", 79.99, 4.7),
    Product("Monitor", 299.99, 4.3),
]

# Sort by price
sorted_by_price = sorted(products, key=attrgetter("price"))
print("Sorted by price:")
for product in sorted_by_price:
    print(f"  {product}")

# Sort by rating (descending)
sorted_by_rating = sorted(products, key=attrgetter("rating"), reverse=True)
print("\nSorted by rating (best first):")
for product in sorted_by_rating:
    print(f"  {product}")


# Example 5: Grouping and Filtering


class Student:
    def __init__(self, name, grade, subject):
        self.name = name
        self.grade = grade
        self.subject = subject

    def __repr__(self):
        return f"Student('{self.name}', {self.grade}, '{self.subject}')"


students = [
    Student("Alice", "A", "Math"),
    Student("Bob", "B", "Math"),
    Student("Charlie", "A", "Science"),
    Student("Diana", "C", "Math"),
    Student("Eve", "A", "Science"),
    Student("Frank", "B", "Science"),
]

# Group by subject
students_by_subject = sorted(students, key=attrgetter("subject"))
grouped = groupby(students_by_subject, key=attrgetter("subject"))

print("Students grouped by subject:")
for subject, group in grouped:
    print(f"\n{subject}:")
    for student in group:
        print(f"  {student.name} (Grade: {student.grade})")

# Filter A-grade students
get_grade = attrgetter("grade")
a_students = [s for s in students if get_grade(s) == "A"]
print(f"\nA-grade students: {[s.name for s in a_students]}")


# 🔧 Advanced Examples
# Example 6: With Complex Data Structures


class Department:
    def __init__(self, name):
        self.name = name


class Company:
    def __init__(self, name, location):
        self.name = name
        self.location = location


class Employee:
    def __init__(self, name, salary, department, company):
        self.name = name
        self.salary = salary
        self.department = department
        self.company = company

    def __repr__(self):
        return f"Employee('{self.name}', ${self.salary})"


# Create complex nested structure
tech_dept = Department("Technology")
sales_dept = Department("Sales")
google = Company("Google", "Mountain View")
microsoft = Company("Microsoft", "Redmond")

employees = [
    Employee("Alice", 120000, tech_dept, google),
    Employee("Bob", 95000, sales_dept, google),
    Employee("Charlie", 110000, tech_dept, microsoft),
    Employee("Diana", 87000, sales_dept, microsoft),
]

# Complex attribute access
get_company_name = attrgetter("company.name")
get_dept_name = attrgetter("department.name")
get_location = attrgetter("company.location")

# Group by company and department
print("Employee breakdown:")
for emp in employees:
    print(
        f"{emp.name}: {get_company_name(emp)} {get_dept_name(emp)} "
        f"in {get_location(emp)} - ${emp.salary}"
    )

# Find highest paid employee per company
employees_by_company = sorted(employees, key=get_company_name)
for company, group in groupby(employees_by_company, key=get_company_name):
    highest_paid = max(group, key=attrgetter("salary"))
    print(f"Highest paid at {company}: {highest_paid.name} (${highest_paid.salary})")


# Example 7: Error Handling and Edge Cases


class DataPoint:
    def __init__(self, value, metadata=None):
        self.value = value
        self.metadata = metadata


class Metadata:
    def __init__(self, source, timestamp):
        self.source = source
        self.timestamp = timestamp


data_points = [
    DataPoint(42, Metadata("sensor1", "2024-01-01")),
    DataPoint(37, Metadata("sensor2", "2024-01-02")),
    DataPoint(55, None),  # No metadata
]

# Safe attribute access with error handling
get_source = attrgetter("metadata.source")

for i, point in enumerate(data_points):
    try:
        source = get_source(point)
        print(f"Data point {i}: value={point.value}, source={source}")
    except AttributeError:
        print(f"Data point {i}: value={point.value}, source=Unknown (no metadata)")


# ⚡ Performance and Use Cases
# Example 8: Performance Comparison


class Item:
    def __init__(self, value):
        self.value = value


# Create lots of items
items = [Item(i) for i in range(100000)]

# Method 1: Using attrgetter
get_value = attrgetter("value")
start = time.time()
values1 = [get_value(item) for item in items]
time1 = time.time() - start

# Method 2: Direct attribute access
start = time.time()
values2 = [item.value for item in items]
time2 = time.time() - start

# Method 3: Lambda function
start = time.time()
values3 = [lambda x: x.value for x in items]
time3 = time.time() - start

print(f"attrgetter: {time1:.4f}s")
print(f"Direct access: {time2:.4f}s")
print(f"Lambda: {time3:.4f}s")

# attrgetter is particularly useful when you need to pass
# the getter function to other functions like sorted(), max(), etc.

# 🎯 Key Benefits and When to Use
# When attrgetter is most useful:
# Sorting operations: sorted(items, key=attrgetter('price'))
# Data extraction: Converting objects to tuples/lists
# Functional programming: Passing to map(), filter(), etc.
# Grouping operations: With itertools.groupby()
# Performance: Faster than lambda for simple attribute access
# Nested attributes: Clean syntax for deep attribute access


# Example 9: Real-world Data Processing


class LogEntry:
    def __init__(self, timestamp, level, message, module):
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.module = module


logs = [
    LogEntry("2024-01-01 10:00", "ERROR", "Database connection failed", "db"),
    LogEntry("2024-01-01 10:01", "INFO", "User login successful", "auth"),
    LogEntry("2024-01-01 10:02", "ERROR", "API timeout", "api"),
    LogEntry("2024-01-01 10:03", "DEBUG", "Cache hit", "cache"),
]

# Analyze logs by level
get_level = attrgetter("level")
get_module = attrgetter("module")

# Count by level
level_counts = defaultdict(int)
for log in logs:
    level_counts[get_level(log)] += 1

print("Log levels:", dict(level_counts))

# Get all error messages
error_messages = [log.message for log in logs if get_level(log) == "ERROR"]
print("Error messages:", error_messages)

# Group by module
logs_by_module = sorted(logs, key=get_module)
for module, group in groupby(logs_by_module, key=get_module):
    count = len(list(group))
    print(f"Module {module}: {count} logs")

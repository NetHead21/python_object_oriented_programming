"""
operator.methodcaller Comprehensive Tutorial and Examples

This module demonstrates the powerful capabilities of Python's `operator.methodcaller` function,
which provides an efficient way to call methods on objects with predefined arguments and
keyword arguments.

Overview:
---------
The `methodcaller` function returns a callable object that calls the given method on its
operand. It's particularly useful for:
- Calling methods with fixed arguments on collections of objects
- Functional programming patterns where you need to pass method calls
- Performance-critical method calling scenarios
- Data transformation and processing pipelines
- Creating reusable method call patterns

Key Features:
------------
✨ Method calling with positional arguments
✨ Method calling with keyword arguments
✨ Method calling with mixed arguments
✨ Performance optimized for repeated method calls
✨ Clean, readable code for functional operations
✨ Seamless integration with built-in functions (map, filter, etc.)
✨ Type-safe method name validation

Performance Benefits:
--------------------
- Faster than lambda functions for simple method calls
- Memory efficient for large datasets
- Optimized C implementation in CPython
- Reduces function call overhead
- Pre-validates method names at creation time

Use Cases:
----------
1. **Batch Operations**: Apply same method to collection of objects
2. **Data Processing**: Transform collections using method calls
3. **Functional Programming**: Use with map(), filter(), sorted()
4. **API Operations**: Batch method calls on API objects
5. **String Processing**: Bulk string transformations
6. **Collection Management**: Batch operations on containers

"""

from operator import methodcaller
from collections import defaultdict
import time
import sys

# =============================================================================
# Example 1: Basic Method Calling
# =============================================================================
"""
Basic Method Calling with methodcaller

This section demonstrates how to use methodcaller to call methods without
arguments on various objects. This is the simplest form of methodcaller usage.

Key Learning Points:
• methodcaller('method') creates a callable that returns obj.method()
• Works with any object that has the specified method
• Method name validation happens at creation time
• Reusable across different object instances

Use Cases:
• Calling standard methods on collections of objects
• String processing operations
• Container method calls (clear, copy, etc.)
• Boolean method calls (is_digit, is_alpha, etc.)
"""

print("=" * 60)
print("Example 1: Basic Method Calling")
print("=" * 60)

# String method examples
text_samples = ["Hello", "WORLD", "123", "Python3.13", "  spaced  "]

# Create method callers for common string methods
call_upper = methodcaller("upper")
call_lower = methodcaller("lower")
call_strip = methodcaller("strip")
call_isdigit = methodcaller("isdigit")
call_isalpha = methodcaller("isalpha")

print("String transformations:")
for text in text_samples:
    print(f"  Original: '{text}'")
    print(f"    upper(): '{call_upper(text)}'")
    print(f"    lower(): '{call_lower(text)}'")
    print(f"    strip(): '{call_strip(text)}'")
    print(f"    isdigit(): {call_isdigit(text)}")
    print(f"    isalpha(): {call_isalpha(text)}")
    print()

# List method examples
numbers = [[1, 2], [3, 4, 5], [6]]
call_copy = methodcaller("copy")
call_clear = methodcaller("clear")

print("List operations:")
for lst in numbers:
    original = lst.copy()
    copied = call_copy(lst)
    print(f"  Original: {original}")
    print(f"  Copied: {copied}")
    print(f"  Same object: {lst is copied}")  # Should be False
    print()

# =============================================================================
# Example 2: Methods with Arguments
# =============================================================================
"""
Method Calling with Arguments

This section shows how methodcaller can call methods with fixed positional
arguments. This is useful when you want to apply the same operation with
the same parameters to multiple objects.

Key Learning Points:
• methodcaller('method', arg1, arg2) calls obj.method(arg1, arg2)
• Arguments are fixed at creation time
• Can pass multiple positional arguments
• Excellent for batch processing with consistent parameters

Use Cases:
• String manipulation with fixed parameters
• Mathematical operations with constants
• File operations with consistent options
• Data formatting with fixed formats
"""


print("\n" + "=" * 60)
print("Example 2: Methods with Arguments")
print("=" * 60)

# String methods with arguments
text_data = ["apple,banana,cherry", "red;green;blue", "1-2-3-4-5"]

# Create method callers with arguments
split_comma = methodcaller("split", ",")
split_semicolon = methodcaller("split", ";")
split_dash = methodcaller("split", "-")
replace_vowels = methodcaller("replace", "a", "@")

print("String splitting and replacement:")
for text in text_data:
    print(f"  Text: '{text}'")
    if "," in text:
        print(f"    split(','): {split_comma(text)}")
    if ";" in text:
        print(f"    split(';'): {split_semicolon(text)}")
    if "-" in text:
        print(f"    split('-'): {split_dash(text)}")
    print(f"    replace('a', '@'): '{replace_vowels(text)}'")
    print()

# Numeric operations
numbers = [3.14159, 2.71828, 1.41421]
round_2 = methodcaller("__round__", 2)  # Round to 2 decimal places
round_4 = methodcaller("__round__", 4)  # Round to 4 decimal places

print("Number rounding:")
for num in numbers:
    print(f"  {num}")
    print(f"    rounded to 2 places: {round_2(num)}")
    print(f"    rounded to 4 places: {round_4(num)}")
    print()


# =============================================================================
# Example 3: Methods with Keyword Arguments
# =============================================================================
"""
Method Calling with Keyword Arguments

This section demonstrates how methodcaller handles keyword arguments,
providing even more flexibility for method calling patterns.

Key Learning Points:
• methodcaller('method', key=value) calls obj.method(key=value)
• Can mix positional and keyword arguments
• Keyword arguments are fixed at creation time
• Useful for methods with many optional parameters

Use Cases:
• String formatting with fixed options
• File operations with specific modes
• Configuration method calls
• API calls with standard parameters
"""

print("\n" + "=" * 60)
print("Example 3: Methods with Keyword Arguments")
print("=" * 60)

# String formatting examples
text_samples = ["hello world", "PYTHON programming", "Data Science"]

# String methods with keyword arguments
center_20 = methodcaller("center", 25, "*")
ljust_20 = methodcaller("ljust", 25, "-")
rjust_20 = methodcaller("rjust", 25, "=")

print("String alignment with custom fill characters:")
for text in text_samples:
    print(f"  Original: '{text}'")
    print(f"    center(25, '*'): '{center_20(text)}'")
    print(f"    ljust(25, '-'): '{ljust_20(text)}'")
    print(f"    rjust(25, '='): '{rjust_20(text)}'")
    print()

# Dictionary operations
sample_dicts = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25, "city": "NYC"},
    {"name": "Charlie", "age": 35, "city": "LA", "job": "Engineer"},
]

get_with_default = methodcaller("get", "city", "Unknown")
pop_with_default = methodcaller("pop", "job", "Unemployed")

print("Dictionary operations with defaults:")
for i, d in enumerate(sample_dicts):
    d_copy = d.copy()  # Work with copy to preserve original
    print(f"  Dict {i + 1}: {d}")
    print(f"    get('city', 'Unknown'): '{get_with_default(d_copy)}'")
    # Note: pop modifies the dictionary, so we use a copy
    job = methodcaller("pop", "job", "Unemployed")(d_copy.copy())
    print(f"    pop('job', 'Unemployed'): '{job}'")
    print()

# =============================================================================
# Example 4: Functional Programming Applications
# =============================================================================
"""
Functional Programming with methodcaller

This section shows how methodcaller excels in functional programming
contexts, particularly with map(), filter(), and other higher-order functions.

Key Learning Points:
• methodcaller integrates seamlessly with map(), filter(), sorted()
• Creates clean, readable functional code
• Avoids lambda boilerplate for simple method calls
• Better performance than equivalent lambda expressions

Use Cases:
• Data transformation pipelines
• Collection processing
• Filtering operations based on method results
• Sorting by method return values
"""

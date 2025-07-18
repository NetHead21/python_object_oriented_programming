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

print("\n" + "=" * 60)
print("Example 4: Functional Programming Applications")
print("=" * 60)

# Data transformation with map()
words = ["hello", "WORLD", "PyThOn", "programming", "DATA"]

# Transform words using various string methods
print("Data transformation with map():")
print(f"Original words: {words}")
print(f"All uppercase: {list(map(methodcaller('upper'), words))}")
print(f"All lowercase: {list(map(methodcaller('lower'), words))}")
print(f"Title case: {list(map(methodcaller('title'), words))}")
print(f"Capitalized: {list(map(methodcaller('capitalize'), words))}")
print(f"Swapped case: {list(map(methodcaller('swapcase'), words))}")
print()

# Filtering with method results
mixed_strings = ["123", "abc", "12a", "456", "xyz", "789abc", "000"]

print("Filtering based on method results:")
print(f"All strings: {mixed_strings}")
print(f"Only digits: {list(filter(methodcaller('isdigit'), mixed_strings))}")
print(f"Only alphabetic: {list(filter(methodcaller('isalpha'), mixed_strings))}")
print(f"Only alphanumeric: {list(filter(methodcaller('isalnum'), mixed_strings))}")
print()


# Sorting by method results
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_age(self):
        return self.age

    def get_name_length(self):
        return len(self.name)

    def get_initials(self):
        return "".join(word[0].upper() for word in self.name.split())

    def __repr__(self):
        return f"Person('{self.name}', {self.age})"


people = [
    Person("Alice Johnson", 30),
    Person("Bob Smith", 25),
    Person("Charlie Brown", 35),
    Person("Diana Prince", 28),
]

print("Sorting people by method results:")
print(f"Original: {people}")
print(f"By age: {sorted(people, key=methodcaller('get_age'))}")
print(f"By name length: {sorted(people, key=methodcaller('get_name_length'))}")
print(f"By initials: {sorted(people, key=methodcaller('get_initials'))}")
print()

# =============================================================================
# Example 5: Batch String Processing
# =============================================================================
"""
Batch String Processing Applications

This section demonstrates methodcaller's power for batch string processing
operations, showing real-world text processing scenarios.

Key Learning Points:
• Efficient batch processing of text data
• Consistent string transformations across datasets
• Pipeline-friendly string operations
• Performance benefits for large text datasets

Use Cases:
• Data cleaning and normalization
• Text preprocessing for analysis
• Batch formatting operations
• Content management systems
"""

print("\n" + "=" * 60)
print("Example 5: Batch String Processing")
print("=" * 60)

# Sample text data (like what you might get from a CSV or database)
user_data = [
    "  Alice@example.com  ",
    "BOB@COMPANY.CO.UK",
    "charlie.brown@university.edu   ",
    "  DIANA_PRINCE@AGENCY.GOV  ",
    "eve.wilson@startup.io",
]

# Text cleaning pipeline
clean_strip = methodcaller("strip")
clean_lower = methodcaller("lower")
normalize_dots = methodcaller("replace", "_", ".")

print("Email cleaning pipeline:")
print("Original emails:")
for email in user_data:
    print(f"  '{email}'")

print("\nAfter strip():")
stripped = list(map(clean_strip, user_data))
for email in stripped:
    print(f"  '{email}'")

print("\nAfter lower():")
lowered = list(map(clean_lower, stripped))
for email in lowered:
    print(f"  '{email}'")

print("\nAfter replace('_', '.'):")
normalized = list(map(normalize_dots, lowered))
for email in normalized:
    print(f"  '{email}'")

# Text analysis
sample_texts = [
    "Hello, World! How are you today?",
    "Python is amazing for data science.",
    "The quick brown fox jumps over the lazy dog.",
    "Machine learning and AI are transforming industries.",
]

# Analysis methods
count_words = methodcaller("split")
count_chars = methodcaller("__len__")
find_python = methodcaller("find", "Python")
starts_with_the = methodcaller("startswith", "The")

print("\nText analysis:")
for text in sample_texts:
    words = count_words(text)
    print(f"Text: '{text}'")
    print(f"  Word count: {len(words)}")
    print(f"  Character count: {count_chars(text)}")
    print(f"  Contains 'Python' at position: {find_python(text)}")
    print(f"  Starts with 'The': {starts_with_the(text)}")
    print()

# =============================================================================
# Example 6: Container Operations
# =============================================================================
"""
Container and Collection Operations

This section shows how methodcaller works with various container types
and their methods, demonstrating batch operations on data structures.

Key Learning Points:
• methodcaller works with any object method
• Useful for batch container operations
• Can manipulate collections uniformly
• Excellent for data structure transformations

Use Cases:
• Batch list/set/dict operations
• Container method standardization
• Data structure pipeline operations
• Collection management tasks
"""

print("\n" + "=" * 60)
print("Example 6: Container Operations")
print("=" * 60)

# List operations
list_samples = [[1, 2, 3], [4, 5], [6, 7, 8, 9], [10]]

# List method callers
get_length = methodcaller("__len__")
copy_list = methodcaller("copy")
reverse_list = methodcaller("reverse")  # Note: this modifies the list

print("List operations:")
for lst in list_samples:
    original = lst.copy()
    print(f"  Original: {original}")
    print(f"    Length: {get_length(lst)}")
    print(f"    Copy: {copy_list(lst)}")

    # Demonstrate reverse (on a copy to preserve original)
    lst_copy = copy_list(lst)
    reverse_list(lst_copy)
    print(f"    Reversed: {lst_copy}")
    print()


# Set operations
set_samples = [{1, 2, 3}, {2, 3, 4, 5}, {4, 5, 6}, {1, 6, 7, 8}]

copy_set = methodcaller("copy")
pop_element = methodcaller("pop")  # Removes and returns arbitrary element

print("Set operations:")
base_set = {1, 2, 3, 4, 5}
print(f"Base set for intersection: {base_set}")

for s in set_samples:
    s_copy = copy_set(s)
    intersection_result = methodcaller("intersection", base_set)(s)
    union_result = methodcaller("union", base_set)(s)

    print(f"  Set: {s}")
    print(f"    Intersection with base: {intersection_result}")
    print(f"    Union with base: {union_result}")

    # Demonstrate pop on copy
    if s_copy:
        popped = pop_element(s_copy)
        print(f"    After pop(): removed {popped}, remaining: {s_copy}")
    print()


# Dictionary operations
dict_samples = [{"a": 1, "b": 2}, {"b": 3, "c": 4, "d": 5}, {"c": 6, "d": 7, "e": 8}]

get_keys = methodcaller("keys")
get_values = methodcaller("values")
get_items = methodcaller("items")

print("Dictionary operations:")
for d in dict_samples:
    print(f"  Dict: {d}")
    print(f"    Keys: {list(get_keys(d))}")
    print(f"    Values: {list(get_values(d))}")
    print(f"    Items: {list(get_items(d))}")
    print()


# =============================================================================
# Example 7: Performance Comparison
# =============================================================================
"""
Performance Analysis of methodcaller

This section provides empirical performance comparison between methodcaller
and alternative approaches like lambda functions and direct method calls.

Key Learning Points:
• methodcaller performance vs. alternatives
• When performance differences matter
• Memory efficiency considerations
• Scale-dependent performance characteristics

Use Cases:
• Performance-critical method calling
• Large dataset operations
• Benchmarking and optimization decisions
• Understanding trade-offs in functional programming
"""

print("\n" + "=" * 60)
print("Example 7: Performance Comparison")
print("=" * 60)

# Create large dataset for performance testing
large_strings = [f"test_string_{i}" for i in range(100000)]

# Method 1: Using methodcaller
upper_caller = methodcaller("upper")
start = time.time()
result1 = [upper_caller(s) for s in large_strings]
time1 = time.time() - start

# Method 2: Direct method calls
start = time.time()
result2 = [s.upper() for s in large_strings]
time2 = time.time() - start

# Method 3: Lambda function with map
start = time.time()
result3 = list(map(lambda s: s.upper(), large_strings))
time3 = time.time() - start

# Method 4: methodcaller with map
start = time.time()
result4 = list(map(methodcaller("upper"), large_strings))
time4 = time.time() - start

print("Performance comparison (100,000 string operations):")
print(f"  methodcaller (list comp): {time1:.4f}s")
print(f"  Direct method calls: {time2:.4f}s")
print(f"  Lambda with map: {time3:.4f}s")
print(f"  methodcaller with map: {time4:.4f}s")


# Verify results are identical
print(f"Results identical: {result1 == result2 == result3 == result4}")

# Memory efficiency test
caller_obj = methodcaller("upper")


def create_upper_function():
    """Create equivalent function for comparison."""
    return lambda s: s.upper()


lambda_obj = create_upper_function()

print("\nMemory usage:")
print(f"  methodcaller object size: {sys.getsizeof(caller_obj)} bytes")
print(f"  lambda object size: {sys.getsizeof(lambda_obj)} bytes")


# =============================================================================
# Example 8: Error Handling and Edge Cases
# =============================================================================
"""
Error Handling and Edge Cases with methodcaller

This section explores how methodcaller behaves with edge cases, error
conditions, and various object types.

Key Learning Points:
• Common error types: AttributeError, TypeError
• Method name validation at creation time
• Graceful error handling strategies
• Type safety considerations

Use Cases:
• Robust data processing pipelines
• Handling inconsistent object types
• Defensive programming practices
• Input validation and sanitization
"""

print("\n" + "=" * 60)
print("Example 8: Error Handling and Edge Cases")
print("=" * 60)

# Test with various object types
mixed_objects = ["hello", [1, 2, 3], {"key": "value"}, 42, None]


# Method callers that might fail on some objects
call_upper = methodcaller("upper")  # Only works on strings
call_append = methodcaller("append", "new_item")  # Only works on lists
call_keys = methodcaller("keys")  # Only works on dicts

print("Testing method calls on different object types:")
for i, obj in enumerate(mixed_objects):
    print(f"  Object {i}: {obj} (type: {type(obj).__name__})")

    # Test upper() method
    try:
        result = call_upper(obj)
        print(f"    upper(): '{result}'")
    except AttributeError as e:
        print(f"    upper(): Error - {e}")

    # Test append() method
    try:
        obj_copy = obj.copy() if hasattr(obj, "copy") else obj
        call_append(obj_copy)
        print("    append('new_item'): Success")
    except (AttributeError, TypeError) as e:
        print(f"    append('new_item'): Error - {type(e).__name__}")

    # Test keys() method
    try:
        result = call_keys(obj)
        print(f"    keys(): {list(result)}")
    except AttributeError as e:
        print(f"    keys(): Error - {type(e).__name__}")

    print()


# Method name validation
print("Method name validation:")
try:
    # This should work
    valid_caller = methodcaller("upper")
    print("  methodcaller('upper'): Created successfully")
except Exception as e:
    print(f"  methodcaller('upper'): Error - {e}")

try:
    # This should fail - method name must be string
    invalid_caller = methodcaller(123)
    print("  methodcaller(123): Created successfully")
except TypeError as e:
    print(f"  methodcaller(123): Error - {e}")


# Safe method calling helper
def safe_method_call(caller, obj, default=None):
    """Safely call a method, returning default if it fails."""
    try:
        return caller(obj)
    except (AttributeError, TypeError):
        return default


# Demonstrate safe calling
safe_upper = methodcaller("upper")
safe_objects = ["hello", 123, None, [1, 2, 3]]

print("\nSafe method calling:")
for obj in safe_objects:
    result = safe_method_call(safe_upper, obj, "N/A")
    print(f"  safe_upper({obj}): {result}")


# =============================================================================
# Example 9: Real-world Use Case - Data Processing Pipeline
# =============================================================================
"""
Real-world Application: Data Processing Pipeline

This section demonstrates a practical, real-world application of methodcaller
for building data processing pipelines. This example shows how methodcaller
can be used in production scenarios.

Key Learning Points:
• Building reusable processing pipelines
• Integration with other Python tools
• Processing structured data efficiently
• Creating maintainable data transformation code

Use Cases:
• ETL (Extract, Transform, Load) operations
• Data cleaning and normalization
• API response processing
• Configuration data processing
• Batch data transformations
"""

print("\n" + "=" * 60)
print("Example 9: Real-world Use Case - Data Processing Pipeline")
print("=" * 60)

# Simulate raw data from a CSV or API
raw_user_data = [
    "  John.Doe@Company.COM  ",
    "jane_smith@university.EDU",
    "BOB.WILSON@AGENCY.GOV   ",
    "alice-jones@startup.io",
    "  CHARLIE.BROWN@CORP.NET",
]


# Data processing pipeline using methodcaller
class DataProcessor:
    """A data processing pipeline using methodcaller for transformations."""

    def __init__(self):
        # Create reusable method callers
        self.strip_whitespace = methodcaller("strip")
        self.to_lowercase = methodcaller("lower")
        self.normalize_dots = methodcaller("replace", "_", ".")
        self.normalize_dashes = methodcaller("replace", "-", ".")
        self.split_at_sign = methodcaller("split", "@")
        self.split_dot = methodcaller("split", ".")

    def clean_email(self, email):
        """Clean and normalize an email address."""
        # Pipeline: strip -> lowercase -> normalize separators
        cleaned = self.strip_whitespace(email)
        cleaned = self.to_lowercase(cleaned)
        cleaned = self.normalize_dots(cleaned)
        cleaned = self.normalize_dashes(cleaned)
        return cleaned

    def extract_domain_info(self, email):
        """Extract domain information from email."""
        parts = self.split_at_sign(email)
        if len(parts) != 2:
            return None

        username, domain = parts
        domain_parts = self.split_dot(domain)

        return {
            "username": username,
            "domain": domain,
            "domain_parts": domain_parts,
            "tld": domain_parts[-1] if domain_parts else None,
            "is_edu": domain.endswith(".edu"),
            "is_gov": domain.endswith(".gov"),
            "is_commercial": domain.endswith((".com", ".co.uk", ".io", ".net")),
        }

    def process_batch(self, email_list):
        """Process a batch of emails."""
        results = []
        for email in email_list:
            cleaned = self.clean_email(email)
            domain_info = self.extract_domain_info(cleaned)

            results.append(
                {"original": email, "cleaned": cleaned, "domain_info": domain_info}
            )

        return results


# Process the data
processor = DataProcessor()
processed_data = processor.process_batch(raw_user_data)

print("Email processing pipeline results:")
for i, result in enumerate(processed_data, 1):
    print(f"\nEmail {i}:")
    print(f"  Original: '{result['original']}'")
    print(f"  Cleaned: '{result['cleaned']}'")

    if result["domain_info"]:
        info = result["domain_info"]
        print(f"  Username: {info['username']}")
        print(f"  Domain: {info['domain']}")
        print(f"  TLD: {info['tld']}")
        print("  Type: ", end="")

        if info["is_edu"]:
            print("Educational")
        elif info["is_gov"]:
            print("Government")
        elif info["is_commercial"]:
            print("Commercial")
        else:
            print("Other")

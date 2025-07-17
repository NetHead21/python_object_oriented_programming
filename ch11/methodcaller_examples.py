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

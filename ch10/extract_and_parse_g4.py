"""
Functional Programming Approach to Log Parsing

This module demonstrates a functional programming approach to log parsing using
Python's built-in functional tools: map(), filter(), and lambda functions.
It showcases how to create a processing pipeline using functional programming
paradigms instead of generator expressions.

The functional pipeline:
1. map(pattern.match, source) - Apply regex to all lines
2. filter(None, matches) - Remove non-matching lines
3. map(lambda m: m.groupdict(), matches) - Extract named groups
4. filter(lambda g: g["level"] == "WARNING", groups) - Filter warnings
5. map(datetime_conversion, warnings) - Convert timestamps
6. map(iso_formatting, datetimes) - Format as ISO strings

Functions:
    extract_and_parse_g4: Extract warnings using functional programming
    demonstrate_functional_pipeline: Show functional approach step by step
    main: Entry point for standalone execution
"""

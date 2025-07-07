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

import csv
import re
from pathlib import Path
import datetime


def extract_and_parse_g4(full_log_path: Path, warning_log_path: Path) -> int:
    """
    Extract warning messages using functional programming approach.

    Demonstrates how to use map(), filter(), and lambda functions to create
    a processing pipeline for log data. This approach emphasizes functional
    programming concepts and immutable data transformations.

    Args:
        full_log_path (Path): Path to the input log file
        warning_log_path (Path): Path to the output CSV file

    Returns:
        int: Number of warning messages extracted

    Raises:
        FileNotFoundError: If the input log file doesn't exist
        PermissionError: If unable to write to output file
        UnicodeDecodeError: If log file contains invalid encoding
        ValueError: If datetime parsing fails

    Functional Pipeline:
        1. map() - Apply transformations to all elements
        2. filter() - Select elements matching criteria
        3. lambda - Define inline transformation functions

    Example:
        >>> count = extract_and_parse_g4(Path('app.log'), Path('warnings.csv'))
        >>> print(f"Processed {count} warnings using functional programming")

    Note:
        This approach emphasizes immutable transformations and functional
        composition, making the code more declarative and easier to reason about.
    """
    if not full_log_path.exists():
        raise FileNotFoundError(f"Log file not found: {full_log_path}")

    # Ensure output directory exists
    warning_log_path.parent.mkdir(parents=True, exist_ok=True)
    warning_count = 0

    with warning_log_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        # Write header row
        writer.writerow(["iso_timestamp", "level", "message"])
        # Enhanced regex pattern with flexible day matching
        pattern = re.compile(
            r"(?P<dt>\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2})"
            r"\s+(?P<level>\w+)"
            r"\s+(?P<msg>.*)"
        )
        with full_log_path.open(encoding="utf-8") as source:
            # Functional programming pipeline using map(), filter(), and lambda
            # Step 1: Strip whitespace and filter empty lines
            clean_lines = filter(lambda line: line.strip(), source)
            # Step 2: Apply regex pattern to all lines
            possible_match_iter = map(pattern.match, map(str.strip, clean_lines))
            # Step 3: Filter out None matches (lines that didn't match pattern)
            good_match_iter = filter(None, possible_match_iter)
            # Step 4: Extract named groups as dictionaries
            group_iter = map(lambda m: m.groupdict(), good_match_iter)
            # Step 5: Filter for WARNING level messages (exact match)
            warnings_iter = filter(lambda g: g.get("level") == "WARNING", group_iter)
            # Step 6: Parse datetime and convert to structured tuple
            dt_iter = map(
                lambda g: (
                    datetime.datetime.strptime(g["dt"], "%b %d, %Y %H:%M:%S"),
                    g["level"],
                    g["msg"],
                ),
                warnings_iter,
            )
            # Step 7: Format datetime as ISO string
            warnings_filter = map(lambda g: (g[0].isoformat(), g[1], g[2]), dt_iter)
            # Process each warning through the functional pipeline
            for warning_tuple in warnings_filter:
                writer.writerow(warning_tuple)
                warning_count += 1

    return warning_count


def demonstrate_functional_pipeline(full_log_path: Path) -> None:
    """
    Demonstrate the functional programming pipeline with detailed output.

    Shows how each step in the functional pipeline transforms the data,
    emphasizing the declarative nature of functional programming.

    Args:
        full_log_path (Path): Path to the input log file
    """
    if not full_log_path.exists():
        print(f"❌ Log file not found: {full_log_path}")
        return
    print("🔧 Functional Programming Pipeline Demonstration:")
    print("=" * 55)

    pattern = re.compile(
        r"(?P<dt>\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2})"
        r"\s+(?P<level>\w+)"
        r"\s+(?P<msg>.*)"
    )

    with full_log_path.open(encoding="utf-8") as source:
        # Take first 10 lines for demonstration
        sample_lines = [line for line in source if line.strip()][:10]

        print(f"📝 Step 1: Input lines ({len(sample_lines)}):")
        for i, line in enumerate(sample_lines[:3], 1):
            print(f"   {i}. {line.strip()[:60]}...")

        print("\n🔍 Step 2: Apply regex pattern (map)")
        matches = list(map(pattern.match, map(str.strip, sample_lines)))
        successful_matches = [m for m in matches if m]
        print(f"   Successful matches: {len(successful_matches)}/{len(sample_lines)}")

        print("\n📦 Step 3: Extract groups (map + lambda)")
        groups = list(map(lambda m: m.groupdict(), successful_matches))
        print(f"   Extracted groups: {len(groups)}")
        for i, group in enumerate(groups[:2], 1):
            print(f"   {i}. {group}")

        print("\n⚠️  Step 4: Filter warnings (filter + lambda)")
        warnings = list(filter(lambda g: g.get("level") == "WARNING", groups))
        print(f"   Warning messages: {len(warnings)}")

        print("\n🕐 Step 5: DateTime conversion (map + lambda)")
        if warnings:
            dt_converted = list(
                map(
                    lambda g: (
                        datetime.datetime.strptime(g["dt"], "%b %d, %Y %H:%M:%S"),
                        g["level"],
                        g["msg"],
                    ),
                    warnings[:2],  # Just first 2 for demo
                )
            )

            print(f"   Converted {len(dt_converted)} timestamps:")
            for i, (dt, level, msg) in enumerate(dt_converted, 1):
                print(f"   {i}. {dt} -> {dt.isoformat()}")


def compare_approaches() -> None:
    """
    Compare functional programming vs generator approaches.
    """
    print("\n🔄 Functional vs Generator Comparison:")
    print("=" * 40)

    print("📊 Functional Programming (map/filter/lambda):")
    print("   ✓ Declarative - describes what, not how")
    print("   ✓ Composable - easy to chain operations")
    print("   ✓ Immutable - no side effects")
    print("   ✓ Readable - clear transformation steps")
    print("   ✓ Testable - each step can be tested independently")

    print("\n📊 Generator Expressions:")
    print("   ✓ Memory efficient - lazy evaluation")
    print("   ✓ Pythonic - more idiomatic Python style")
    print("   ✓ Concise - fewer function calls")
    print("   ✓ Performance - generally faster for large datasets")

    print("\n🎯 When to use each:")
    print("   Functional: When emphasizing clarity and testability")
    print("   Generators: When prioritizing memory efficiency and performance")

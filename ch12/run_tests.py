#!/usr/bin/env python3
"""Test runner script for GPS message parsing system.

This script runs all tests and provides a summary of the test results.
"""

import unittest
import sys
import os

# Add the current directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_tests():
    """Run all GPS message parsing tests."""
    # Discover and load all tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName("test_gps_message_slots")

    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2, descriptions=True, failfast=False, buffer=True
    )

    print("=" * 70)
    print("GPS Message Parsing System - Test Suite")
    print("=" * 70)

    result = runner.run(suite)

    print("\n" + "=" * 70)
    print("Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.wasSuccessful():
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)

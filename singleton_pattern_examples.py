"""
Singleton Design Pattern Examples

This module demonstrates the Singleton design pattern through practical examples:
1. Database Connection Manager
2. Application Logger
3. Configuration Manager
4. Cache Manager

The Singleton pattern ensures that a class has only one instance and provides
a global point of access to that instance. This is useful when you need to
coordinate actions across a system from a single point.

Key Characteristics:
    - Only one instance can exist
    - Global access point to the instance
    - Lazy initialization (created when first needed)
    - Thread-safe implementation considerations

When to Use:
    - Database connection pools
    - Logging systems
    - Configuration managers
    - Caching systems
    - Hardware interface access
    - GUI application instances
"""

import threading
import time
from typing import Optional, Dict, Any


# =============================================================================
# Basic Singleton Implementation
# =============================================================================


class BasicSingleton:
    """
    Basic Singleton implementation using __new__ method.

    This is the simplest way to implement Singleton in Python.
    Uses the __new__ method to control instance creation.
    """

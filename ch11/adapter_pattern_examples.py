"""
Adapter Design Pattern - Real-World Examples

The Adapter pattern allows incompatible interfaces to work together.
It acts as a bridge between two incompatible interfaces by wrapping
one interface to make it compatible with another.

Key Characteristics:
    - Allows incompatible interfaces to work together
    - Wraps existing functionality with a new interface
    - Enables legacy code integration without modification
    - Acts as a translator between different APIs

When to Use:
    - Integrating third-party libraries with different interfaces
    - Working with legacy systems
    - Making incompatible APIs work together
    - Converting data formats or protocols
"""

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Dict, List, Any

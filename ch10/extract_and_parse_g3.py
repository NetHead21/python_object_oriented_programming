"""
Advanced DateTime Log Parser with Generator Chains

This module demonstrates an advanced log parsing approach using generator chains
with datetime processing. It showcases how to parse timestamps, convert them to
datetime objects, and format them as ISO strings for standardized output.

The generator chain includes:
1. Pattern matching with named groups
2. Dictionary extraction from matches
3. Filtering for WARNING level messages
4. DateTime parsing and conversion
5. ISO format timestamp generation

Functions:
    extract_and_parse_g3: Extract warnings with datetime processing
    demonstrate_datetime_parsing: Show datetime conversion process
    main: Entry point for standalone execution

Author: Python OOP Tutorial
Date: July 2025
"""

import datetime
import csv
import re
from pathlib import Path

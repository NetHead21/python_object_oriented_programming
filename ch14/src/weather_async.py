"""Asynchronous Marine Weather Forecast Fetcher.

This module demonstrates concurrent HTTP requests using asyncio and httpx to
fetch marine weather forecasts from NOAA's National Weather Service. It showcases:
    - Async/await pattern for concurrent I/O operations
    - asyncio.gather() for parallel task execution
    - httpx.AsyncClient for async HTTP requests
    - Named tuples for structured data
    - Regular expressions for text parsing

Key Features:
    - Concurrent fetching of 13 Chesapeake Bay marine forecasts
    - Significant speedup vs sequential requests (~13x faster)
    - Async HTTP client with automatic connection pooling
    - Advisory extraction from forecast text using regex
    - Clean resource management with async context managers

Data Source:
    National Weather Service (NWS) Marine Forecasts
    - Base URL: https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/an/
    - Format: Plain text forecasts with structured headers
    - Zones: Chesapeake Bay and Tidal Potomac areas
    - Update frequency: Multiple times daily

Performance:
    Sequential execution: ~13 seconds (1 second per forecast)
    Concurrent execution: ~1-2 seconds (all forecasts in parallel)
    Speedup factor: ~7-13x depending on network conditions

Concurrency Model:
    Uses asyncio event loop with:
    - One task per forecast zone (13 concurrent tasks)
    - httpx.AsyncClient for connection pooling and keep-alive
    - asyncio.gather() to await all tasks simultaneously
    - Single-threaded async I/O (no thread/process overhead)

Example Output:
    Chesapeake Bay from Pooles Island to Sandy Point, MD SMALL CRAFT ADVISORY
    Chesapeake Bay from Sandy Point to North Beach, MD SMALL CRAFT ADVISORY
    ...
    Got 13 forecasts in 1.234 seconds

Use Cases:
    - Weather monitoring applications
    - Marine navigation systems
    - Demonstrating async HTTP patterns
    - Performance comparison: async vs sync I/O

Dependencies:
    - asyncio: Built-in async framework
    - httpx: Modern async HTTP client (pip install httpx)
    - re: Built-in regular expression module
    - time: Built-in timing utilities

Network Requirements:
    - Internet connection to reach tgftp.nws.noaa.gov
    - HTTPS support (port 443)
    - No authentication required (public data)

Error Handling:
    Current implementation assumes:
    - Network availability (no retry logic)
    - Server responsiveness (no timeout handling)
    - Valid response format (no validation)

    Production use should add:
    - try/except around HTTP requests
    - Timeout configuration
    - Retry logic with exponential backoff
    - Response validation
"""

import asyncio
import httpx
import re
import time
from urllib.request import urlopen
from typing import Optional, NamedTuple


class Zone(NamedTuple):
    """Marine forecast zone with NWS identification codes.

    Represents a geographic zone for which NOAA NWS issues marine weather
    forecasts. Each zone has a human-readable name and standardized codes
    for identification in various systems.

    This NamedTuple provides:
    - Immutable zone data (thread-safe)
    - Tuple unpacking support
    - Hash-ability (can be used in sets/dicts)
    - Low memory footprint compared to classes
    - Automatic __repr__, __eq__, etc.

    Attributes:
        zone_name (str): Human-readable zone description.
            Example: "Chesapeake Bay from Pooles Island to Sandy Point, MD"
        zone_code (str): NWS alphanumeric zone identifier.
            Format: ANZnnn where nnn is a 3-digit number
            Example: "ANZ531" (AN=Coastal/Marine, Z=Zone, 531=specific area)
        same_code (str): Special Area Messaging Encoder (SAME) code.
            Format: 6-digit code used in emergency alert systems
            Example: "073531" (07=Maryland, 3531=specific zone)

    Code Systems:
        - Zone Code (ANZ): Used in URLs and forecast headers
        - SAME Code: Used in NOAA Weather Radio and EAS broadcasts
        - Both uniquely identify the geographic forecast area

    Properties:
        forecast_url: Dynamically generates the NWS forecast URL for this zone

    Example:
        >>> zone = Zone(
        ...     zone_name="Chesapeake Bay from Pooles Island to Sandy Point, MD",
        ...     zone_code="ANZ531",
        ...     same_code="073531"
        ... )
        >>> print(zone.zone_name)
        Chesapeake Bay from Pooles Island to Sandy Point, MD
        >>> print(zone.forecast_url)
        https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/an/anz531.txt

    Immutability:
        >>> zone.zone_code = "ANZ999"  # Raises AttributeError
        AttributeError: can't set attribute

    Tuple Operations:
        >>> name, code, same = zone  # Unpacking
        >>> zone[0]  # Index access
        'Chesapeake Bay from Pooles Island to Sandy Point, MD'
        >>> len(zone)  # Length
        3

    Note:
        Zone codes and SAME codes are standardized by NOAA and don't change
        frequently, making them reliable identifiers for automated systems.
    """

    zone_name: str
    zone_code: str
    same_code: str  # Special Area Messaging Encoder

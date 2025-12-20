"""Multi-threaded Weather Data Fetcher for Canadian Cities.

This module demonstrates concurrent I/O using Python's threading module to
fetch current temperature data from Environment Canada's weather service.
It showcases:
    - Thread-based concurrency for I/O-bound operations
    - XML parsing with ElementTree
    - Named tuples for structured data
    - Thread coordination with start() and join()
    - Significant performance improvement over sequential requests

Key Features:
    - Concurrent fetching of 13 Canadian city temperatures
    - XML parsing from Environment Canada's CityPage Weather API
    - Thread-safe data collection in separate Thread instances
    - ~13x speedup compared to sequential HTTP requests
    - Simple thread coordination without locks (write-once pattern)

Data Source:
    Environment and Climate Change Canada (ECCC)
    - Base URL: https://dd.weather.gc.ca/citypage_weather/xml/
    - Format: XML documents with current conditions
    - Coverage: Major cities across all Canadian provinces/territories
    - Update frequency: Hourly or more frequently
    - Free public API (no authentication required)

Performance:
    Sequential execution: ~13 seconds (1 second per city)
    Threaded execution: ~1-2 seconds (all cities in parallel)
    Speedup factor: ~7-13x depending on network conditions

Concurrency Model:
    Uses threading module with:
    - One thread per city (13 concurrent threads)
    - Each thread performs blocking I/O independently
    - Main thread coordinates with start() and join()
    - No shared mutable state (thread-safe by design)
    - GIL doesn't matter (I/O-bound, not CPU-bound)

Example Output:
    Currently 5°C in Charlottetown
    Currently -15°C in Edmonton
    Currently 2°C in Fredericton
    ...
    Got 13 temps in 1.234 seconds

Use Cases:
    - Weather monitoring dashboards
    - Learning threading fundamentals
    - Demonstrating I/O-bound concurrency
    - Performance comparison: threads vs sequential vs async

Dependencies:
    - threading: Built-in threading module
    - urllib.request: Built-in HTTP client
    - xml.etree.ElementTree: Built-in XML parser
    - time: Built-in timing utilities

Network Requirements:
    - Internet connection to reach dd.weather.gc.ca
    - HTTPS support (port 443)
    - No authentication required (public data)
    - Reliable service from Environment Canada

Threading vs Async:
    This module uses threads for concurrency. Compare with async version:

    Threads (this module):
    - Pros: Simple model, works with blocking I/O, familiar paradigm
    - Cons: Thread overhead (~1MB per thread), GIL limitations for CPU work
    - Best for: I/O-bound with blocking libraries, mixed sync/async code

    Async (weather_async.py):
    - Pros: Lower overhead, more scalable, modern paradigm
    - Cons: Requires async libraries, different mental model
    - Best for: Pure I/O-bound, many concurrent operations (100+)

Thread Safety:
    - Each thread writes to its own self.temperature attribute
    - Main thread reads after join() ensures completion
    - No locks needed due to write-once, read-after pattern
    - Safe even without GIL protection

Error Handling:
    Current implementation:
    - Catches and displays XML parse errors
    - Prints raw XML for debugging
    - Re-raises exceptions (will terminate program)
    - No retry logic or timeouts

    Production enhancements:
    - Add timeout to urlopen() calls
    - Graceful handling of network errors
    - Retry logic with exponential backoff
    - Validation of XML structure

Comparison with weather_async.py:
    Both fetch weather data concurrently but use different approaches:
    - weather_threads.py: Threading (this module)
    - weather_async.py: Asyncio with httpx

    Performance is similar for 13 requests, but async scales better
    for 100+ concurrent operations.
"""

from threading import Thread
import time
from urllib.request import urlopen
from xml.etree import ElementTree
from typing import Optional, NamedTuple


class Station(NamedTuple):
    """Weather station identifier for Environment Canada's API.

    Represents a weather monitoring station with its location code and
    language preference for data retrieval. This immutable data structure
    provides URL generation for fetching weather data.

    NamedTuple Benefits:
    - Immutable: Thread-safe without synchronization
    - Lightweight: Lower memory footprint than classes
    - Tuple operations: Unpacking, indexing, iteration
    - Built-in methods: __repr__, __eq__, __hash__
    - Type hints: Static type checking support

    Attributes:
        province (str): Two-letter province/territory code.
            Examples: "ON" (Ontario), "BC" (British Columbia), "QC" (Quebec)
            Full list: AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT
        code (str): Station identifier assigned by Environment Canada.
            Format: s followed by 7 digits (e.g., "s0000458")
            Unique identifier for each monitoring station
        language (str, optional): Language code for data format.
            "e" - English (default)
            "f" - French (français)
            Affects text descriptions, not numerical data

    Properties:
        path: Relative path component for API URL
        url: Complete HTTPS URL for fetching XML weather data

    Example:
        >>> station = Station(province="ON", code="s0000458", language="e")
        >>> station.province
        'ON'
        >>> station.url
        'https://dd.weather.gc.ca/citypage_weather/xml/ON/s0000458_e.xml'

        >>> # French version
        >>> station_fr = Station("QC", "s0000620", "f")
        >>> station_fr.url
        'https://dd.weather.gc.ca/citypage_weather/xml/QC/s0000620_f.xml'

    Tuple Operations:
        >>> province, code, lang = station  # Unpacking
        >>> station[0]  # Index access
        'ON'
        >>> len(station)
        3

    Thread Safety:
        Fully thread-safe due to immutability. Multiple threads can safely
        access the same Station instance without synchronization.

    API Structure:
        Environment Canada organizes data by:
        1. Province/Territory (2-letter code)
        2. Station code (7-digit identifier)
        3. Language (e or f)
        4. Format (XML in this case)

    Note:
        Station codes are stable identifiers but may occasionally change
        if monitoring stations are relocated or decommissioned. Check
        Environment Canada's documentation for current codes.
    """

    province: str
    code: str
    language: str = "e"  # "f" for French

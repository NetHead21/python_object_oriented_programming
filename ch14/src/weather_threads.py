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

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

    @property
    def path(self) -> str:
        """Generate the relative path component for the weather XML URL.

        Constructs the path following Environment Canada's URL structure:
        /{province}/{code}_{language}.xml

        Returns:
            str: Relative path starting with / for the weather data XML.

        Format:
            /{province}/     # Two-letter province/territory code
            {code}_          # Seven-digit station identifier
            {language}.xml   # Language code and file extension

        Example:
            >>> station = Station("ON", "s0000458", "e")
            >>> station.path
            '/ON/s0000458_e.xml'

            >>> station_french = Station("QC", "s0000620", "f")
            >>> station_french.path
            '/QC/s0000620_f.xml'

        Usage:
            This path is combined with the base URL to create the complete
            endpoint for fetching weather data. It's separated as a property
            to enable alternative base URLs (e.g., local mirrors, testing).

        Note:
            The path always starts with / to be used as an absolute path
            component in URL construction.
        """

        return f"/{self.province}/{self.code}_{self.language}.xml"

    @property
    def url(self) -> str:
        """Generate the complete HTTPS URL for fetching weather XML data.

        Constructs the full URL to Environment Canada's CityPage Weather
        service by combining the base URL with the station's path.

        Returns:
            str: Complete HTTPS URL to the weather data XML document.

        URL Structure:
            https://dd.weather.gc.ca/       # Base URL (DataMart)
            citypage_weather/xml            # Service path
            /{province}/{code}_{lang}.xml   # Station-specific path

        Example:
            >>> station = Station("ON", "s0000458", "e")
            >>> station.url
            'https://dd.weather.gc.ca/citypage_weather/xml/ON/s0000458_e.xml'

        DataMart Service:
            dd.weather.gc.ca is Environment Canada's DataMart service:
            - Public access (no authentication)
            - HTTPS protocol (secure)
            - High availability
            - Updated frequently (typically hourly)
            - Free for non-commercial and commercial use

        Response Format:
            The URL returns an XML document containing:
            - Current conditions (temperature, humidity, wind, etc.)
            - Forecast data (short-term and long-term)
            - Weather warnings and watches
            - Station metadata (location, elevation, etc.)
            - Observation timestamp

        Network Access:
            - Protocol: HTTPS (port 443)
            - Method: GET (via urlopen)
            - No authentication required
            - Typical response time: 200-800ms
            - Response size: 50-200 KB

        Alternative Base URLs:
            For testing or redundancy, you might use:
            - Local mirror: http://localhost/weather/xml{self.path}
            - Alternative server: https://backup.example.com{self.path}

        Note:
            This property computes the URL on each access. For repeated
            use, consider caching the result:
            ```python
            url = station.url  # Cache it
            for _ in range(10):
                fetch_data(url)  # Reuse cached URL
            ```
        """

        return f"https://dd.weather.gc.ca/citypage_weather/xml{self.path}"


# Major Canadian cities with their weather station identifiers
# Source: Environment and Climate Change Canada (ECCC)
# One city per province/territory (13 total)
#
# Geographic Coverage:
# - All 10 provinces: AB, BC, MB, NB, NL, NS, ON, PE, QC, SK
# - All 3 territories: NT, NU, YT
#
# Selection Criteria:
# - Capital or largest city in each region
# - Active weather monitoring stations
# - Reliable data availability
# - Representative climate for the region
#
# Station Codes:
# Format: s{7-digit number}
# Assigned by Environment Canada
# Stable but may change if stations relocate
#
# Usage:
#     station = CITIES["Toronto"]
#     url = station.url  # Get weather data URL
#

CITIES = {
    "Charlottetown": Station("PE", "s0000583"),  # Prince Edward Island capital
    "Edmonton": Station("AB", "s0000045"),  # Alberta capital
    "Fredericton": Station("NB", "s0000250"),
    "Halifax": Station("NS", "s0000318"),
    "Iqaluit": Station("NU", "s0000394"),
    "Québec City": Station("QC", "s0000620"),
    "Regina": Station("SK", "s0000788"),
    "St. John's": Station("NL", "s0000280"),
    "Toronto": Station("ON", "s0000458"),
    "Victoria": Station("BC", "s0000775"),
    "Whitehorse": Station("YT", "s0000825"),
    "Winnipeg": Station("MB", "s0000193"),
    "Yellowknife": Station("NT", "s0000366"),
}


class TempGetter(Thread):
    """Thread subclass for fetching temperature data from a weather station.

    Extends threading.Thread to perform concurrent HTTP requests and XML
    parsing for temperature retrieval. Each instance fetches data for one
    city independently.

    This design demonstrates:
    - Thread subclassing (run() method override)
    - Thread-safe data storage (write-once pattern)
    - Blocking I/O in separate thread
    - XML parsing with error handling
    - Clean separation of concerns

    Thread Lifecycle:
        1. __init__: Initialize thread with city name
        2. start(): Launch thread (calls run() in new thread)
        3. run(): Fetch and parse data (executes in thread)
        4. join(): Wait for completion (called from main thread)
        5. Access temperature: Read result after join()

    Attributes:
        city (str): Human-readable city name (e.g., "Toronto")
        station (Station): Weather station configuration
        temperature (Optional[str]): Temperature value or None/"(missing)"
            - None: Before run() executes
            - "(missing)": Temperature tag not found in XML
            - "{value}": Numeric temperature string (e.g., "5", "-15")

    Thread Safety:
        Safe without locks because:
        - Each thread writes only to its own instance attributes
        - Main thread reads only after join() (guarantees completion)
        - No shared mutable state between threads
        - Write-once pattern (temperature written once, read after)

    Example:
        >>> thread = TempGetter("Toronto")
        >>> thread.start()  # Launches thread
        >>> thread.join()   # Waits for completion
        >>> print(thread.temperature)
        '5'
        >>> print(f"Currently {thread.temperature}°C in {thread.city}")
        Currently 5°C in Toronto

    Concurrent Usage:
        >>> threads = [TempGetter(city) for city in CITIES]
        >>> for t in threads:
        ...     t.start()  # All threads running concurrently
        >>> for t in threads:
        ...     t.join()   # Wait for all to complete
        >>> for t in threads:
        ...     print(f"{t.city}: {t.temperature}°C")

    Error Handling:
        - XML parse errors: Caught, printed, and re-raised
        - Network errors: Not caught (will terminate thread)
        - Missing tags: Sets temperature to "(missing)"
        - Thread exceptions: Silently fail (check with is_alive())

    Performance:
        - Thread creation: ~1ms overhead
        - Network I/O: 200-1000ms (varies by network)
        - XML parsing: <10ms typically
        - Thread cleanup: <1ms
        - Total per thread: ~200-1000ms (I/O dominated)

    Alternative Designs:
        Could use threading with queue:
        ```python
        def fetch_temp(city, queue):
            # ... fetch temperature ...
            queue.put((city, temperature))

        threads = [Thread(target=fetch_temp, args=(city, q))
                   for city in CITIES]
        ```

        Or use ThreadPoolExecutor:
        ```python
        with ThreadPoolExecutor(max_workers=13) as executor:
            futures = {executor.submit(fetch_temp, city): city
                      for city in CITIES}
            results = {city: future.result()
                      for future, city in futures.items()}
        ```

    Note:
        Inherits from Thread rather than using Thread(target=...) pattern
        for cleaner encapsulation of city and result data.
    """

    def __init__(self, city: str) -> None:
        """Initialize temperature fetcher thread for a specific city.

        Args:
            city (str): City name, must exist in CITIES dictionary.

        Raises:
            KeyError: If city not found in CITIES dictionary.

        Side Effects:
            - Calls Thread.__init__() to initialize threading machinery
            - Stores city name and station configuration
            - Initializes temperature to None

        Example:
            >>> thread = TempGetter("Toronto")
            >>> thread.city
            'Toronto'
            >>> thread.station.province
            'ON'
            >>> thread.temperature  # Not yet fetched
            None

            >>> # Invalid city raises KeyError
            >>> thread = TempGetter("InvalidCity")
            KeyError: 'InvalidCity'

        Thread State:
            After initialization, thread is in "new" state:
            - Not yet started
            - No system resources allocated
            - Can be started with start() method

        Note:
            Must call super().__init__() to properly initialize the
            Thread base class before the thread can be started.
        """

        super().__init__()
        self.city = city
        self.station = CITIES[self.city]
        self.temperature: Optional[str] = None

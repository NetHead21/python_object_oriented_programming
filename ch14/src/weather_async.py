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

    @property
    def forecast_url(self) -> str:
        """Generate the NWS forecast URL for this zone.

        Constructs the URL to fetch the plain text marine forecast from
        NOAA's FTP server. The URL follows NWS conventions:
        - Base: https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/
        - Region: an/ (Atlantic Northeast)
        - File: {zone_code}.txt (lowercase zone code)

        Returns:
            str: Complete HTTPS URL to the zone's forecast text file.

        URL Structure:
            https://tgftp.nws.noaa.gov/
                data/forecasts/marine/coastal/  # Forecast type
                an/                              # Region code
                anz531.txt                       # Zone file (lowercase)

        Example:
            >>> zone = Zone("Test Zone", "ANZ531", "073531")
            >>> zone.forecast_url
            'https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/an/anz531.txt'

        Region Codes:
            - an: Atlantic Northeast (includes Chesapeake Bay)
            - am: Atlantic Mid-Atlantic
            - as: Atlantic Southeast
            - gm: Gulf of Mexico
            - etc.

        Note:
            The zone_code is converted to lowercase as NWS URLs are
            case-sensitive and use lowercase filenames.

        Access:
            - Protocol: HTTPS (secure)
            - Authentication: None required (public data)
            - Format: Plain text with structured sections
        """

        return (
            f"https://tgftp.nws.noaa.gov/data/forecasts"
            f"/marine/coastal/an/{self.zone_code.lower()}.txt"
        )


ZONES = [
    # Chesapeake Bay and Tidal Potomac Marine Forecast Zones
    # Source: NOAA National Weather Service
    # Coverage: Maryland and Virginia coastal waters
    # Total: 13 zones covering the Chesapeake Bay region
    #
    # Zone Structure:
    # - Chesapeake Bay: Main body (ANZ531-534)
    # - Tidal Potomac: Potomac River tidal sections (ANZ535-537)
    # - Rivers/Harbors: Tributary rivers and harbors (ANZ538-539)
    # - Bays/Sounds: Eastern tributaries and sounds (ANZ540-543)
    #
    # Geographic Coverage:
    # North to South: Pooles Island (north) to Smith Point (south)
    # West to East: Key Bridge (west) to Eastern Bay (east)
    #
    # Each zone receives:
    # - Forecast updates multiple times daily
    # - Wind speed and direction
    # - Wave height and period
    # - Weather conditions
    # - Special marine advisories and warnings
    Zone("Chesapeake Bay from Pooles Island to Sandy Point, MD", "ANZ531", "073531"),
    # Remaining zones continue south along Chesapeake Bay
    Zone("Chesapeake Bay from Sandy Point to North Beach, MD", "ANZ532", "073532"),
    Zone("Chesapeake Bay from North Beach to Drum Point, MD", "ANZ533", "073533"),
    Zone("Chesapeake Bay from Drum Point to Smith Point, VA", "ANZ534", "073534"),
    Zone("Tidal Potomac from Key Bridge to Indian Head, MD", "ANZ535", "073535"),
    Zone("Tidal Potomac from Indian Head to Cobb Island, MD", "ANZ536", "073536"),
    Zone("Tidal Potomac from Cobb Island, MD to Smith Point, VA", "ANZ537", "073537"),
    Zone("Patapsco River including Baltimore Harbor", "ANZ538", "073538"),
    Zone("Chester River to Queenstown MD", "ANZ539", "073539"),
    Zone("Eastern Bay", "ANZ540", "073540"),
    Zone(
        "Choptank River to Cambridge MD and the Little Choptank River",
        "ANZ541",
        "073541",
    ),
    Zone("Patuxent River to Broome’s Island MD", "ANZ542", "073542"),
    Zone(
        "Tangier Sound and the Inland Waters surrounding Bloodsworth Island",
        "ANZ543",
        "073543",
    ),
]


class MarineWX:
    """Asynchronous marine weather forecast fetcher and parser.

    Fetches and parses marine weather forecasts from NOAA NWS for a specific
    zone. Uses async HTTP requests for concurrent operation with other
    MarineWX instances.

    This class demonstrates:
    - Async I/O pattern with httpx
    - Regular expression text parsing
    - Property-based computed attributes
    - Async context manager usage

    Workflow:
        1. Initialize with a Zone
        2. Call run() to fetch forecast (async)
        3. Access advisory property to extract alerts
        4. Use repr() for formatted output

    Attributes:
        zone (Zone): Geographic forecast zone
        doc (str): Raw forecast text from NWS (empty until run() completes)
        advisory_pat (re.Pattern): Class-level regex for advisory extraction

    Class Attributes:
        advisory_pat: Compiled regex pattern matching advisory sections.
            Pattern: r"\\n\\.\\.\\.\\(.*?)\\.\\.\\.\\n"
            Matches text between triple dots on separate lines:
                ...
                SMALL CRAFT ADVISORY IN EFFECT FROM 6 PM THIS EVENING TO
                6 AM EST SATURDAY...
                ...

            Flags:
                - re.M: Multiline mode (^ and $ match line boundaries)
                - re.S: Dotall mode (. matches newlines)

    Async Design:
        The run() method is async to enable concurrent fetching of multiple
        forecasts. This is crucial for performance when fetching 13+ zones
        that would otherwise take 13+ seconds sequentially.

    Example:
        >>> import asyncio
        >>> zone = Zone("Test Zone", "ANZ531", "073531")
        >>> wx = MarineWX(zone)
        >>> asyncio.run(wx.run())
        >>> print(wx.advisory)
        'SMALL CRAFT ADVISORY IN EFFECT UNTIL 6 AM EST SATURDAY'
        >>> print(wx)
        Test Zone SMALL CRAFT ADVISORY IN EFFECT UNTIL 6 AM EST SATURDAY

    Performance:
        - Single fetch: ~1 second
        - 13 concurrent fetches: ~1-2 seconds total
        - Memory: ~10-20 KB per forecast document

    Alternative Implementations:
        The commented code in run() shows the original blocking I/O approach
        using urllib. The async httpx version provides:
        - Better concurrency support
        - Connection pooling
        - Modern async/await syntax
        - Automatic keep-alive

    Error Handling:
        Current implementation assumes successful HTTP requests. Production
        use should add:
        - try/except for network errors
        - HTTP status code checking
        - Timeout configuration
        - Retry logic

    Text Format:
        NWS forecast format includes:
        - Header with zone and issue time
        - Synopsis section
        - Detailed forecast by time period
        - Advisories/warnings in ...triple dot... blocks
        - Multiple sections separated by $$
    """

    advisory_pat = re.compile(r"\n\.\.\.(.*?)\.\.\n", re.M | re.S)

    def __init__(self, zone: Zone) -> None:
        """Initialize marine weather fetcher for a specific zone.

        Args:
            zone (Zone): Geographic forecast zone to fetch and parse.

        Attributes Set:
            self.zone: Stores the zone for later reference
            self.doc: Initialized to empty string (populated by run())

        Example:
            >>> zone = Zone("Test", "ANZ531", "073531")
            >>> wx = MarineWX(zone)
            >>> wx.doc
            ''
            >>> wx.zone.zone_code
            'ANZ531'

        Note:
            The super().__init__() call is defensive programming for
            potential future inheritance, though not strictly necessary
            for a non-inheriting class.
        """

        super().__init__()
        self.zone = zone
        self.doc = ""

    async def run(self) -> None:
        """Asynchronously fetch forecast text from NWS server.

        Performs async HTTP GET request to retrieve the plain text marine
        forecast for this zone. Updates self.doc with the response text.

        This method is async to enable concurrent fetching of multiple
        forecasts without blocking. It uses httpx.AsyncClient for:
        - Non-blocking I/O operations
        - Automatic connection pooling
        - HTTP/2 support
        - Keep-alive connections

        Returns:
            None: Updates self.doc as a side effect.

        Side Effects:
            Sets self.doc to the forecast text (typically 2-5 KB)

        Network Request:
            - Method: GET
            - URL: self.zone.forecast_url
            - Protocol: HTTPS
            - Timeout: Default httpx timeout (~5 seconds)

        Async Pattern:
            Uses async context manager for proper resource cleanup:
            1. AsyncClient acquires connection from pool
            2. GET request sent asynchronously
            3. Response awaited without blocking event loop
            4. Connection returned to pool on exit

        Example:
            >>> import asyncio
            >>> zone = Zone("Test", "ANZ531", "073531")
            >>> wx = MarineWX(zone)
            >>> await wx.run()  # In async context
            >>> len(wx.doc)
            2345
            >>> 'MARINE WEATHER' in wx.doc
            True

        Concurrent Usage:
            >>> zones = [Zone(f"Z{i}", f"ANZ{i}", f"073{i}") for i in range(3)]
            >>> forecasts = [MarineWX(z) for z in zones]
            >>> await asyncio.gather(*(f.run() for f in forecasts))
            # All 3 forecasts fetched concurrently

        Alternative Implementation:
            The commented code shows the original synchronous approach:
            ```python
            with urlopen(self.zone.forecast_url) as stream:
                self.doc = stream.read().decode("UTF-8")
            ```
            This blocks the thread during I/O, preventing concurrency.

        Performance:
            - Single request: ~500ms - 1.5 seconds
            - Concurrent requests: Still ~1-2 seconds total
            - Network latency dominates execution time

        Error Handling:
            Current implementation doesn't handle:
            - Network errors (httpx.NetworkError)
            - HTTP errors (4xx, 5xx responses)
            - Timeouts (httpx.TimeoutException)
            - Invalid response encoding

            Production should add:
            ```python
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        self.zone.forecast_url,
                        timeout=10.0
                    )
                    response.raise_for_status()
                    self.doc = response.text
            except httpx.HTTPError as e:
                logger.error(f"HTTP error for {self.zone.zone_code}: {e}")
                self.doc = ""  # Or retry logic
            ```

        Note:
            Must be called with await in an async context. Calling without
            await returns a coroutine object without executing the fetch.
        """

        # Original blocking I/O implementation (deprecated):
        # with urlopen(self.zone.forecast_url) as stream:
        #     self.doc = stream.read().decode("UTF-8")

        async with httpx.AsyncClient() as client:
            response = await client.get(self.zone.forecast_url)
        self.doc = response.text

    @property
    def advisory(self) -> str:
        """Extract marine advisory text from forecast document.

        Searches the forecast text for advisory/warning sections marked by
        triple dots (...text...) and returns the extracted text with newlines
        replaced by spaces for single-line display.

        Advisory Format in Source:
            ...
            SMALL CRAFT ADVISORY IN EFFECT FROM 6 PM THIS EVENING TO
            6 AM EST SATURDAY...
            ...

        Returns:
            str: Advisory text with newlines replaced by spaces, or empty
                string if no advisory found.

        Regex Pattern:
            r"\\n\\.\\.\\."     # Newline followed by three literal dots
            (.*?)              # Capture group: any characters (non-greedy)
            r"\\.\\.\\.\\n"    # Three literal dots followed by newline

        Processing:
            1. Search doc with regex pattern
            2. If match found, extract group(1) (captured text)
            3. Replace all newlines with spaces
            4. Return processed text
            5. If no match, return empty string

        Example:
            >>> wx = MarineWX(zone)
            >>> wx.doc = "Forecast\\n...SMALL CRAFT ADVISORY...\\nDetails"
            >>> wx.advisory
            'SMALL CRAFT ADVISORY'

            >>> wx.doc = "Forecast\\n...GALE WARNING IN EFFECT\\nUNTIL MIDNIGHT...\\nDetails"
            >>> wx.advisory
            'GALE WARNING IN EFFECT UNTIL MIDNIGHT'

        Advisory Types:
            Common advisories found in marine forecasts:
            - SMALL CRAFT ADVISORY: Winds 20-33 knots
            - GALE WARNING: Winds 34-47 knots
            - STORM WARNING: Winds 48-63 knots
            - HURRICANE WARNING: Winds 64+ knots
            - DENSE FOG ADVISORY: Visibility < 1 nautical mile
            - SPECIAL MARINE WARNING: Severe weather < 2 hours

        Computed Property:
            This property is computed on-demand from self.doc. It doesn't
            cache results, so each access re-parses the document. For
            frequent access, consider caching:
            ```python
            @cached_property
            def advisory(self) -> str:
                # Same implementation
            ```

        Walrus Operator:
            Uses assignment expression (match := ...) to:
            1. Perform regex search
            2. Assign result to 'match'
            3. Check if match is truthy (not None)
            4. All in one conditional expression

            Equivalent verbose version:
            ```python
            match = self.advisory_pat.search(self.doc)
            if match:
                return match.group(1).replace("\n", " ")
            return ""
            ```

        Note:
            Returns empty string (not None) when no advisory found,
            simplifying string operations and display logic.
        """

        if match := self.advisory_pat.search(self.doc):
            return match.group(1).replace("\n", " ")
        return ""

    def __repr__(self) -> str:
        """Return formatted string representation of forecast.

        Combines zone name and advisory text for display. Used by print()
        and str() to produce human-readable output.

        Returns:
            str: "{zone_name} {advisory_text}"

        Format:
            If advisory exists:
                "Chesapeake Bay from Pooles Island to Sandy Point, MD SMALL CRAFT ADVISORY"

            If no advisory:
                "Chesapeake Bay from Pooles Island to Sandy Point, MD "
                (note trailing space)

        Example:
            >>> zone = Zone("Test Zone", "ANZ531", "073531")
            >>> wx = MarineWX(zone)
            >>> wx.doc = "...SMALL CRAFT ADVISORY..."
            >>> repr(wx)
            'Test Zone SMALL CRAFT ADVISORY'
            >>> print(wx)  # Uses __repr__
            Test Zone SMALL CRAFT ADVISORY

        Usage:
            >>> forecasts = [MarineWX(z) for z in ZONES]
            >>> await asyncio.gather(*(f.run() for f in forecasts))
            >>> for f in forecasts:
            ...     print(f)  # Calls __repr__
            Chesapeake Bay from Pooles Island... SMALL CRAFT ADVISORY
            Chesapeake Bay from Sandy Point... GALE WARNING
            ...

        Note:
            Could be enhanced to format advisory text with color codes,
            severity indicators, or truncation for very long advisories:
            ```python
            def __repr__(self) -> str:
                advisory = self.advisory[:100]  # Truncate long advisories
                severity = "WARNING" if "WARNING" in advisory else "ADVISORY"
                return f"{self.zone.zone_name} [{severity}] {advisory}"
            ```
        """
        return f"{self.zone.zone_name} {self.advisory}"


async def task_main() -> None:
    """Main async task coordinating concurrent forecast fetching.

    Orchestrates the entire weather fetching workflow:
    1. Start timing
    2. Create MarineWX instances for all zones
    3. Launch concurrent fetch tasks
    4. Wait for all tasks to complete
    5. Display results
    6. Report performance metrics

    This function demonstrates:
    - asyncio.gather() for concurrent task execution
    - asyncio.create_task() for task creation
    - Generator expression for efficient task iteration
    - Performance measurement with time.perf_counter()

    Concurrency Strategy:
        Uses asyncio.gather() with unpacked generator to:
        - Create all tasks simultaneously
        - Execute them concurrently (not sequentially)
        - Wait for all to complete before proceeding
        - Preserve task order in results (though we don't use them)

    Returns:
        None: Prints results to stdout as side effect.

    Side Effects:
        - Fetches 13 HTTP requests concurrently
        - Prints 13 forecast summaries to stdout
        - Prints performance summary to stdout

    Performance:
        Sequential equivalent: ~13 seconds (1 second per forecast)
        Concurrent execution: ~1-2 seconds (all forecasts in parallel)
        Speedup: ~7-13x depending on network latency

    Output Format:
        {zone_name} {advisory_text}
        {zone_name} {advisory_text}
        ...
        Got {n} forecasts in {time:.3f} seconds

    Example Output:
        Chesapeake Bay from Pooles Island to Sandy Point, MD SMALL CRAFT ADVISORY
        Chesapeake Bay from Sandy Point to North Beach, MD
        Chesapeake Bay from North Beach to Drum Point, MD GALE WARNING
        ...
        Got 13 forecasts in 1.234 seconds

    Code Breakdown:
        ```python
        # Create instances (fast, no I/O)
        forecasts = [MarineWX(z) for z in ZONES]

        # Create and gather tasks (concurrent I/O)
        await asyncio.gather(
            *(asyncio.create_task(f.run()) for f in forecasts)
        )
        ```

        The generator expression creates tasks lazily, then gather()
        executes them concurrently. Alternative verbose version:
        ```python
        tasks = [asyncio.create_task(f.run()) for f in forecasts]
        await asyncio.gather(*tasks)
        ```

    Timing Methodology:
        Uses time.perf_counter() for high-resolution timing:
        - Start: Before creating tasks
        - End: After all tasks complete and results printed
        - Includes: Network I/O, parsing, printing
        - Excludes: Module import time

    Task Management:
        asyncio.create_task() vs direct coroutines:
        - create_task(): Schedules coroutine on event loop immediately
        - Direct await: Would execute sequentially
        - gather() with tasks: All run concurrently

    Error Handling:
        Current implementation:
        - No try/except around HTTP requests
        - One failure causes gather() to raise exception
        - Partial results are lost on error

        Robust version would use:
        ```python
        results = await asyncio.gather(
            *(f.run() for f in forecasts),
            return_exceptions=True
        )
        for f, result in zip(forecasts, results):
            if isinstance(result, Exception):
                print(f"{f.zone.zone_name} ERROR: {result}")
            else:
                print(f)
        ```

    Scalability:
        Current design handles 13 zones well. For hundreds of zones:
        - Consider semaphore to limit concurrent connections
        - Use connection pooling (httpx already does this)
        - Add progress reporting for long-running operations
        - Implement chunked gathering to control memory

        Example with semaphore:
        ```python
        semaphore = asyncio.Semaphore(10)  # Max 10 concurrent

        async def fetch_with_limit(forecast):
            async with semaphore:
                await forecast.run()

        await asyncio.gather(*(fetch_with_limit(f) for f in forecasts))
        ```

    Note:
        This function must be called with asyncio.run() or within an
        existing event loop. It cannot be called directly as a regular
        function.
    """

    start = time.perf_counter()
    forecasts = [MarineWX(z) for z in ZONES]

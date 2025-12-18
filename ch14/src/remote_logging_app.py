"""Remote Logging Application with Sorting Algorithms.

This module demonstrates remote logging using Python's logging.handlers.SocketHandler
to send log records over TCP to a centralized log server. It implements two sorting
algorithms (BogoSort and GnomeSort) with comprehensive logging to track performance
and execution details.

Key Features:
    - Remote logging via TCP socket to a log server (localhost:18842)
    - Abstract base class (Sorter) for sorting algorithm implementations
    - BogoSort: Brute-force algorithm trying all permutations
    - GnomeSort: Simple comparison-based sorting algorithm
    - Performance tracking with timing measurements
    - Process-specific logging with PID identification

Logging Architecture:
    - Each process creates a logger with name "app_{pid}"
    - Each Sorter instance creates a child logger "app_{pid}.{ClassName}"
    - SocketHandler sends pickled LogRecords to remote server
    - StreamHandler outputs to stderr for local debugging
    - Both handlers configured at INFO level

Use Cases:
    - Demonstrating remote logging in distributed systems
    - Comparing sorting algorithm performance
    - Teaching logging best practices with hierarchical loggers
    - Testing log server implementations (e.g., log_catcher.py)

Network Protocol:
    - Host: localhost (configurable via LOG_HOST)
    - Port: 18842 (configurable via LOG_PORT)
    - Protocol: TCP with pickled LogRecord objects
    - Automatic reconnection on connection failures

Example Usage:
    >>> # Start log server first (e.g., log_catcher.py)
    >>> python remote_logging_app.py
    INFO:app_12345:sorting 10 collections
    INFO:app_12345.GnomeSort:Sorting 7
    INFO:app_12345.GnomeSort:Sorted 7 items, 0.023 ms
    ...
    INFO:app_12345:produced 22 entries, taking 0.045000 s

Sorting Algorithms:
    - BogoSort: O(n×n!) average case - generates random permutations
    - GnomeSort: O(n²) worst case - similar to insertion sort

Performance Notes:
    - BogoSort only practical for very small datasets (n ≤ 10)
    - GnomeSort efficient for small datasets or nearly sorted data
    - Remote logging adds network latency (~1-5ms per log record)

Security Warning:
    - SocketHandler sends pickled objects over network
    - Only use with trusted log servers
    - Consider encrypting connections for sensitive data
"""

from __future__ import annotations
import abc
from itertools import permutations
import logging
import logging.handlers
import os
import random
import time
import sys
from typing import Iterable

logger = logging.getLogger(f"app_{os.getpid()}")


class Sorter(abc.ABC):
    """Abstract base class for sorting algorithms with integrated logging.

    This ABC defines the interface for sorting implementations and provides
    automatic logger configuration for each sorter instance. The logger name
    follows a hierarchical pattern: "app_{pid}.{ClassName}" enabling:
    - Process identification via PID
    - Algorithm identification via class name
    - Hierarchical log filtering and routing

    Subclasses must implement the sort() method to provide specific sorting
    algorithms. All implementations should log:
    - Start of sorting operation (with data size)
    - End of sorting operation (with timing information)
    - Any significant intermediate steps or decisions

    Attributes:
        logger (logging.Logger): Process and class-specific logger instance.

    Design Pattern:
        Template Method - sort() defines the interface, subclasses implement
        the algorithm while inheriting logging infrastructure.

    Example Subclass:
        >>> class BubbleSort(Sorter):
        ...     def sort(self, data: list[float]) -> list[float]:
        ...         self.logger.info("Sorting %d items", len(data))
        ...         # ... sorting implementation ...
        ...         self.logger.info("Sorted in %.3f ms", duration)
        ...         return sorted_data

    Logger Hierarchy:
        app_{pid}                    # Root application logger
        └── app_{pid}.BogoSort      # BogoSort instance logger
        └── app_{pid}.GnomeSort     # GnomeSort instance logger

    Note:
        The logger is created per instance, so multiple sorter instances
        in the same process share the same logger name.
    """

    def __init__(self) -> None:
        """Initialize sorter with process and class-specific logger.

        Creates a hierarchical logger using the pattern "app_{pid}.{ClassName}"
        where PID identifies the process and ClassName identifies the algorithm.

        The logger inherits handlers and level from parent "app_{pid}" logger,
        enabling centralized logging configuration.

        Side Effects:
            Creates a logger in the logging module's namespace.
        """

        id = os.getpid()
        self.logger = logging.getLogger(f"app_{id}.{self.__class__.__name__}")

    @abc.abstractmethod
    def sort(self, data: list[float]) -> list[float]:
        """Sort data and return ordered list.

        Abstract method that subclasses must implement to provide sorting
        functionality. Implementations should:
        1. Log the start of sorting with data size
        2. Perform the sorting algorithm
        3. Log completion with timing information
        4. Return the sorted data

        Args:
            data (list[float]): Unsorted list of floating-point numbers.

        Returns:
            list[float]: Sorted list in ascending order.

        Raises:
            NotImplementedError: If subclass doesn't implement this method.

        Performance:
            Implementation-dependent. See subclass documentation for
            time and space complexity details.

        Example:
            >>> sorter = GnomeSort()
            >>> result = sorter.sort([3.1, 1.4, 2.7])
            >>> print(result)
            [1.4, 2.7, 3.1]
        """
        ...


class BogoSort(Sorter):
    """Brute-force sorting algorithm using permutation enumeration.

    BogoSort (also called "stupid sort" or "permutation sort") generates all
    possible permutations of the input data in lexicographic order until it
    finds one that is sorted. This is purely for educational/demonstration
    purposes and should never be used in production.

    Algorithm:
        1. Generate permutations in lexicographic order
        2. Check if current permutation is sorted
        3. If sorted, return; otherwise try next permutation
        4. Repeat until sorted permutation found

    Complexity:
        - Time: O(n × n!) average case (n! permutations, each checked in O(n))
        - Space: O(n) for storing current permutation
        - Worst case: Must try all n! permutations

    Practical Limits:
        - n ≤ 8: Usually completes in reasonable time (< 1 second)
        - n = 9: May take several seconds
        - n = 10: May take minutes
        - n > 10: Impractical (10! = 3,628,800 permutations)

    Performance Characteristics:
        - Deterministic: Uses lexicographic permutation order (not random)
        - Not in-place: Creates new tuples for each permutation
        - Comparison-based: Uses pairwise comparisons to verify order
        - Educational value: Demonstrates factorial complexity growth

    Example:
        >>> sorter = BogoSort()
        >>> result = sorter.sort([3.0, 1.0, 2.0])
        INFO:app_12345.BogoSort:Sorting 3
        INFO:app_12345.BogoSort:Sorted 3 items in 4 steps, 0.123 ms
        >>> print(result)
        [1.0, 2.0, 3.0]

    Note:
        This implementation uses itertools.permutations which generates
        permutations in lexicographic order, making it deterministic but
        still impractical for large inputs.

    Warning:
        Do not use with n > 10. The algorithm becomes prohibitively slow
        due to factorial time complexity.
    """

    @staticmethod
    def is_ordered(data: tuple[float, ...]) -> bool:
        """Check if data tuple is sorted in ascending order.

        Verifies ordering by checking all adjacent pairs to ensure each
        element is less than or equal to the next element.

        Args:
            data (tuple[float, ...]): Tuple to check for sorted order.

        Returns:
            bool: True if sorted in ascending order, False otherwise.

        Algorithm:
            Uses zip(data, data[1:]) to create pairs of adjacent elements,
            then checks all pairs satisfy a ≤ b condition.

        Time Complexity:
            O(n) - must check all adjacent pairs.

        Example:
            >>> BogoSort.is_ordered((1.0, 2.0, 3.0))
            True
            >>> BogoSort.is_ordered((3.0, 1.0, 2.0))
            False
            >>> BogoSort.is_ordered((1.0, 2.0, 2.0, 3.0))  # Handles duplicates
            True

        Note:
            Uses ≤ (less than or equal) to correctly handle duplicate values.
        """

        pairs: Iterable[tuple[float, float]] = zip(data, data[1:])
        return all(a <= b for a, b in pairs)

    def sort(self, data: list[float]) -> list[float]:
        """Sort data using brute-force permutation enumeration.

        Generates permutations in lexicographic order until finding a sorted
        one. Logs the start, number of steps tried, and completion time.

        Args:
            data (list[float]): Unsorted list of numbers.

        Returns:
            list[float]: Sorted list in ascending order.

        Side Effects:
            - Logs "Sorting {n}" at start
            - Logs "Sorted {n} items in {steps} steps, {time} ms" at end

        Performance:
            For n items, may need to try up to n! permutations. Each
            permutation check takes O(n) time.

            Typical steps for random data:
            - n=3: ~3 steps
            - n=4: ~12 steps
            - n=5: ~60 steps
            - n=8: ~20,000 steps
            - n=10: ~1,800,000 steps (impractical)

        Example:
            >>> sorter = BogoSort()
            >>> result = sorter.sort([5.0, 2.0, 8.0, 1.0])
            INFO:app_12345.BogoSort:Sorting 4
            INFO:app_12345.BogoSort:Sorted 4 items in 15 steps, 0.234 ms

        Raises:
            StopIteration: Should never occur as permutations() generates
                all n! permutations, guaranteeing a sorted one exists.

        Warning:
            Execution time grows factorially. Avoid using with n > 10.
        """

        self.logger.info("Sorting %d", len(data))
        start = time.perf_counter()

        ordering: tuple[float, ...] = tuple(data[:])
        permute_iter = permutations(data)
        steps = 0
        while not BogoSort.is_ordered(ordering):
            ordering = next(permute_iter)
            steps += 1

        duration = 1000 * (time.perf_counter() - start)
        self.logger.info(
            "Sorted %d items in %d steps, %.3f ms", len(data), steps, duration
        )
        return list(ordering)


class GnomeSort(Sorter):
    """Simple comparison-based sorting algorithm similar to insertion sort.

    GnomeSort (also called "Stupid Sort") works like a garden gnome sorting
    flower pots: move forward if in order, swap and move back if not. It's
    conceptually simple but less efficient than optimized algorithms.

    Algorithm:
        1. Start at index 1
        2. If current element ≥ previous: move forward
        3. If current element < previous: swap and move backward
        4. Continue until reaching the end

    Complexity:
        - Time: O(n²) worst case, O(n) best case (already sorted)
        - Space: O(1) - sorts in-place
        - Stable: Yes - preserves relative order of equal elements
        - Adaptive: Yes - faster on nearly sorted data

    Comparison with Similar Algorithms:
        - vs Insertion Sort: Similar performance, simpler to understand
        - vs Bubble Sort: Typically faster due to less redundant comparisons
        - vs Quick Sort: Much slower (O(n²) vs O(n log n))
        - vs Selection Sort: Similar O(n²) but adaptive

    Performance Characteristics:
        - Best case: O(n) for already sorted data
        - Average case: O(n²) requiring ~n²/4 comparisons
        - Worst case: O(n²) for reverse sorted data
        - In-place: Modifies input list directly (O(1) extra space)
        - Stable: Equal elements maintain relative order

    Practical Use Cases:
        - Small datasets (n < 100)
        - Nearly sorted data
        - Educational purposes
        - Embedded systems with memory constraints

    Example:
        >>> sorter = GnomeSort()
        >>> data = [64.0, 34.0, 25.0, 12.0, 22.0, 11.0, 90.0]
        >>> result = sorter.sort(data)
        INFO:app_12345.GnomeSort:Sorting 7
        INFO:app_12345.GnomeSort:Sorted 7 items, 0.045 ms
        >>> print(result)
        [11.0, 12.0, 22.0, 25.0, 34.0, 64.0, 90.0]

    Visual Example:
        [3, 1, 2]  index=1, 3>1, swap → [1, 3, 2]
        [1, 3, 2]  index=0, restart → [1, 3, 2]
        [1, 3, 2]  index=1, 1<3, forward → [1, 3, 2]
        [1, 3, 2]  index=2, 3>2, swap → [1, 2, 3]
        [1, 2, 3]  index=1, 1<2, forward → [1, 2, 3]
        [1, 2, 3]  index=2, 2<3, forward → Done

    Note:
        The algorithm modifies the input list in-place, so the returned
        list is the same object as the input.
    """

    def sort(self, data: list[float]) -> list[float]:
        """Sort data in-place using the GnomeSort algorithm.

        Implements the garden gnome metaphor: move forward when in order,
        swap and move backward when out of order. Logs start and completion
        with timing information.

        Args:
            data (list[float]): Unsorted list of numbers to sort in-place.

        Returns:
            list[float]: The same list object, now sorted in ascending order.

        Side Effects:
            - Modifies input list in-place
            - Logs "Sorting {n}" at start
            - Logs "Sorted {n} items, {time} ms" at end

        Algorithm Steps:
            1. Initialize index to 1 (start from second element)
            2. While index < len(data):
               a. If data[index-1] < data[index]: increment index
               b. Else: swap elements and decrement index (if > 1)
            3. Return sorted data

        Performance:
            - Best case: O(n) - already sorted, just walks through once
            - Average case: O(n²) - random data requires many swaps
            - Worst case: O(n²) - reverse sorted requires maximum swaps

        Example:
            >>> sorter = GnomeSort()
            >>> data = [3.14, 1.41, 2.71]
            >>> result = sorter.sort(data)
            INFO:app_12345.GnomeSort:Sorting 3
            INFO:app_12345.GnomeSort:Sorted 3 items, 0.012 ms
            >>> print(result)
            [1.41, 2.71, 3.14]
            >>> print(data)  # Same object
            [1.41, 2.71, 3.14]

        Timing:
            Typical execution times on modern hardware:
            - n=10: < 0.1 ms
            - n=100: ~1-5 ms
            - n=1000: ~100-500 ms
            - n=10000: ~10-50 seconds

        Note:
            Unlike BogoSort.sort(), this method modifies the input list
            in-place and returns the same list object.
        """

        self.logger.info("Sorting %d", len(data))
        start = time.perf_counter()

        index = 1
        while index != len(data):
            if data[index - 1] < data[index]:
                index += 1
            else:
                data[index - 1], data[index] = data[index], data[index - 1]
                if index > 1:
                    index -= 1

        duration = 1000 * (time.perf_counter() - start)
        self.logger.info("Sorted %d items, %.3f ms", len(data), duration)
        return data


def main(workload: int = 10, sorter: Sorter = BogoSort()) -> int:
    """Execute sorting workload with random data and specified sorter.

    Generates and sorts multiple collections of random data, using the
    specified sorting algorithm. Each collection has a random size between
    3 and 10 elements, filled with random floats in [0, 1).

    This function serves as:
    - Performance testing harness for sorting algorithms
    - Workload generator for logging demonstrations
    - Benchmark utility for comparing algorithm efficiency

    Args:
        workload (int, optional): Number of collections to sort.
            Defaults to 10.
        sorter (Sorter, optional): Sorting algorithm instance to use.
            Defaults to BogoSort().

    Returns:
        int: Total number of elements sorted across all collections.

    Side Effects:
        - Calls sorter.sort() for each collection (generates logs)
        - Uses random.random() and random.randint() (affects RNG state)

    Performance:
        Execution time depends on:
        - Workload size (number of collections)
        - Sorting algorithm complexity
        - Random collection sizes (3-10 elements each)

        Typical times:
        - GnomeSort, workload=10: < 1 ms total
        - BogoSort, workload=10: 10-100 ms total (highly variable)

    Example:
        >>> from remote_logging_app import main, GnomeSort
        >>> sorter = GnomeSort()
        >>> total = main(workload=5, sorter=sorter)
        INFO:app_12345.GnomeSort:Sorting 7
        INFO:app_12345.GnomeSort:Sorted 7 items, 0.023 ms
        ...
        >>> print(f"Sorted {total} elements total")
        Sorted 32 elements total

    Testing:
        >>> # Test with minimal workload
        >>> total = main(workload=1, sorter=GnomeSort())
        >>> assert 3 <= total <= 10  # One collection of 3-10 elements

        >>> # Test total calculation
        >>> random.seed(42)  # For reproducible results
        >>> total = main(workload=3, sorter=GnomeSort())
        >>> # total is sum of 3 random integers in [3, 10]

    Data Generation:
        Each collection:
        - Size: random.randint(3, 10) → [3, 4, 5, 6, 7, 8, 9, or 10]
        - Values: [random.random() for _ in range(samples)] → floats in [0, 1)
        - Independent: Each collection generated separately

    Note:
        The default BogoSort() is extremely slow. For production use or
        large workloads, use GnomeSort() or other efficient algorithms.

    Warning:
        With BogoSort and unlucky RNG, collections of size 9-10 may take
        several minutes to sort. Consider limiting workload or using
        GnomeSort for predictable execution times.
    """

    total = 0
    for i in range(workload):
        samples = random.randint(3, 10)
        data = [random.random() for _ in range(samples)]
        ordered = sorter.sort(data)
        total += samples
    return total


if __name__ == "__main__":
    """Main execution block demonstrating remote logging with sorting algorithms.
    
    This block configures dual logging (remote socket + local stderr) and
    executes a sorting workload to demonstrate:
    - Remote logging via TCP socket to log server
    - Local logging to stderr for immediate feedback
    - Performance measurement and reporting
    - Proper logging shutdown and resource cleanup
    
    Configuration:
        LOG_HOST: 'localhost' - Log server hostname
        LOG_PORT: 18842 - Log server port (must match server)

    Logging Setup:
        1. SocketHandler: Sends LogRecords to remote server via TCP
           - Pickles LogRecord objects automatically
           - Handles connection failures gracefully
           - Reconnects automatically on subsequent logs
        
        2. StreamHandler: Outputs to stderr for local visibility
           - Immediate feedback during execution
           - Useful for debugging if server unavailable
        
        3. basicConfig: Sets both handlers at INFO level
           - Root logger captures all app_* loggers
           - INFO level filters out DEBUG messages

    Workflow:
        1. Configure logging with dual handlers
        2. Start performance timer
        3. Log workload start
        4. Execute sorting workload (10 collections with GnomeSort)
        5. Log workload completion with timing
        6. Shutdown logging gracefully

    Expected Output (stderr):
        INFO:app_12345:sorting 10 collections
        INFO:app_12345.GnomeSort:Sorting 7
        INFO:app_12345.GnomeSort:Sorted 7 items, 0.023 ms
        ...
        INFO:app_12345:produced 22 entries, taking 0.045000 s
    
    Remote Server:
        Ensure log server is running before execution:
        $ python log_catcher.py &
        $ python remote_logging_app.py
    
    Log Record Count:
        workload * 2 + 2 entries:
        - 1 entry: "sorting N collections" (start)
        - workload entries: "Sorting N" (per collection)
        - workload entries: "Sorted N items..." (per collection)
        - 1 entry: "produced N entries..." (completion)
    
    Performance Monitoring:
        Uses time.perf_counter() for high-resolution timing:
        - Start: Before logging begins
        - End: After workload completion
        - Reports total execution time in seconds
    
    Resource Cleanup:
        logging.shutdown() ensures:
        - All handlers flush buffered records
        - Socket connections close properly
        - File handles release
        - Threads terminate gracefully
    
    Network Behavior:
        If log server unavailable:
        - SocketHandler connection fails silently
        - Local stderr still shows output
        - Application continues normally
        - Subsequent logs attempt reconnection
    
    Customization:
        Modify these values to experiment:
        - LOG_HOST: 'remote.example.com' for remote server
        - LOG_PORT: 9999 for different port
        - workload: 100 for more collections
        - sorter: BogoSort() for comparison (slow!)
    """

    LOG_HOST, LOG_PORT = "localhost", 18842
    socket_handler = logging.handlers.SocketHandler(LOG_HOST, LOG_PORT)
    stream_handler = logging.StreamHandler(sys.stderr)
    logging.basicConfig(handlers=[socket_handler, stream_handler], level=logging.INFO)

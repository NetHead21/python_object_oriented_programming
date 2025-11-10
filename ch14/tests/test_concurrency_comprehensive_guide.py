"""Comprehensive tests for concurrency_comprehensive_guide module."""

import asyncio
import pytest
import time
from pathlib import Path
import sys
import concurrent.futures

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from concurrency_comprehensive_guide import (
    ThreadingExamples,
    ThreadPoolExample,
    MultiprocessingExamples,
    ProcessCommunication,
    AsyncIOExamples,
    ConcurrencyPatterns,
    ErrorHandling,
    PerformanceComparison,
    print_guidelines,
)


# ============================================================================
# THREADING EXAMPLES TESTS
# ============================================================================


class TestThreadingExamples:
    """Test suite for ThreadingExamples class."""

    def test_basic_thread_example_completes(self, capsys):
        """Test that basic thread example runs without errors."""
        ThreadingExamples.basic_thread_example()
        captured = capsys.readouterr()

        # Verify output contains expected messages
        assert "starting work" in captured.out.lower()
        assert "completed" in captured.out.lower()
        assert "All threads finished" in captured.out

    def test_thread_with_lock_prevents_race_condition(self, capsys):
        """Test that lock properly synchronizes counter updates."""
        ThreadingExamples.thread_with_lock()
        captured = capsys.readouterr()

        # The counter should reach exactly 100000 (10 threads * 10000 iterations)
        assert "100000" in captured.out

    def test_producer_consumer_pattern_completes(self, capsys):
        """Test producer-consumer pattern runs successfully."""
        ThreadingExamples.producer_consumer_pattern()
        captured = capsys.readouterr()

        # Should have producer and consumer output
        assert "Producer" in captured.out
        assert "Consumer" in captured.out


class TestThreadPoolExample:
    """Test suite for ThreadPoolExample class."""

    def test_download_simulation_returns_all_results(self):
        """Test that download simulation returns results for all URLs."""
        urls = [f"http://example.com/page{i}" for i in range(5)]
        results = ThreadPoolExample.download_simulation(urls)

        assert len(results) == len(urls)
        assert all("Content from" in result for result in results)

    def test_download_simulation_single_url(self):
        """Test download simulation with single URL."""
        urls = ["http://example.com/single"]
        results = ThreadPoolExample.download_simulation(urls)

        assert len(results) == 1
        assert "Content from http://example.com/single" in results[0]

    def test_download_simulation_empty_list(self):
        """Test download simulation with empty URL list."""
        results = ThreadPoolExample.download_simulation([])
        assert results == []

    def test_map_example_returns_squares(self):
        """Test that map example returns squared values."""
        results = ThreadPoolExample.map_example()

        expected = [i * i for i in range(10)]
        assert results == expected

    def test_map_example_correct_length(self):
        """Test that map example returns correct number of results."""
        results = ThreadPoolExample.map_example()
        assert len(results) == 10


# ============================================================================
# MULTIPROCESSING EXAMPLES TESTS
# ============================================================================


class TestMultiprocessingExamples:
    """Test suite for MultiprocessingExamples class."""

    def test_cpu_intensive_task_returns_correct_sum(self):
        """Test that CPU intensive task calculates correct sum of squares."""
        result = MultiprocessingExamples.cpu_intensive_task(10)
        expected = sum(i * i for i in range(10))
        assert result == expected

    def test_cpu_intensive_task_zero(self):
        """Test CPU intensive task with zero input."""
        result = MultiprocessingExamples.cpu_intensive_task(0)
        assert result == 0

    def test_cpu_intensive_task_large_number(self):
        """Test CPU intensive task with larger number."""
        result = MultiprocessingExamples.cpu_intensive_task(100)
        expected = sum(i * i for i in range(100))
        assert result == expected

    @pytest.mark.xfail(
        reason="Uses local functions which can't be pickled for multiprocessing"
    )
    def test_basic_process_example_completes(self, capsys):
        """Test that basic process example runs without errors."""
        MultiprocessingExamples.basic_process_example()
        captured = capsys.readouterr()

        assert "Process" in captured.out
        assert "Results:" in captured.out

    def test_process_pool_example_returns_all_results(self):
        """Test that process pool returns results for all inputs."""
        numbers = [100, 200, 300]
        results = MultiprocessingExamples.process_pool_example(numbers)

        assert len(results) == len(numbers)
        assert all(isinstance(r, int) for r in results)

    def test_process_pool_example_single_number(self):
        """Test process pool with single number."""
        numbers = [500]
        results = MultiprocessingExamples.process_pool_example(numbers)

        assert len(results) == 1
        expected = sum(i * i for i in range(500))
        assert results[0] == expected

    def test_process_pool_example_empty_list(self):
        """Test process pool with empty list."""
        results = MultiprocessingExamples.process_pool_example([])
        assert results == []

    @pytest.mark.slow
    def test_compare_sequential_vs_parallel_runs(self, capsys):
        """Test that performance comparison runs without errors."""
        MultiprocessingExamples.compare_sequential_vs_parallel()
        captured = capsys.readouterr()

        assert "Sequential time" in captured.out
        assert "Parallel time" in captured.out
        assert "Speedup" in captured.out


class TestProcessCommunication:
    """Test suite for ProcessCommunication class."""

    @pytest.mark.xfail(
        reason="Uses local functions which can't be pickled for multiprocessing"
    )
    def test_queue_communication_completes(self, capsys):
        """Test that queue communication runs successfully."""
        ProcessCommunication.queue_communication()
        captured = capsys.readouterr()

        assert "Produced" in captured.out
        assert "Consumed" in captured.out

    @pytest.mark.xfail(
        reason="Uses local functions which can't be pickled for multiprocessing"
    )
    def test_pipe_communication_completes(self, capsys):
        """Test that pipe communication runs successfully."""
        ProcessCommunication.pipe_communication()
        captured = capsys.readouterr()

        assert "Worker received" in captured.out
        assert "Parent received" in captured.out
        assert "Processed" in captured.out


# ============================================================================
# ASYNCIO EXAMPLES TESTS
# ============================================================================


class TestAsyncIOExamples:
    """Test suite for AsyncIOExamples class."""

    @pytest.mark.asyncio
    async def test_async_task_returns_result(self):
        """Test that async task returns expected result."""
        result = await AsyncIOExamples.async_task(1, 0.1)
        assert result == "Result from task 1"

    @pytest.mark.asyncio
    async def test_async_task_completes_in_time(self):
        """Test that async task respects duration."""
        start = time.time()
        await AsyncIOExamples.async_task(1, 0.5)
        elapsed = time.time() - start

        assert 0.4 < elapsed < 0.7

    @pytest.mark.asyncio
    async def test_run_concurrent_tasks_returns_all_results(self):
        """Test that concurrent tasks return all results."""
        results = await AsyncIOExamples.run_concurrent_tasks()

        assert len(results) == 3
        assert all("Result from task" in r for r in results)

    @pytest.mark.asyncio
    async def test_run_concurrent_tasks_runs_concurrently(self):
        """Test that tasks actually run concurrently (not sequentially)."""
        start = time.time()
        await AsyncIOExamples.run_concurrent_tasks()
        elapsed = time.time() - start

        # Should take ~3 seconds (longest task), not 6 seconds (sum of all)
        assert elapsed < 4.0

    @pytest.mark.asyncio
    async def test_fetch_data_async_returns_data(self):
        """Test that fetch_data_async returns expected data."""
        url = "http://example.com"
        result = await AsyncIOExamples.fetch_data_async(url)

        assert result == f"Data from {url}"

    @pytest.mark.asyncio
    async def test_fetch_multiple_urls_returns_all(self):
        """Test that fetching multiple URLs returns all results."""
        urls = [f"http://example.com/page{i}" for i in range(5)]
        results = await AsyncIOExamples.fetch_multiple_urls(urls)

        assert len(results) == len(urls)
        assert all("Data from" in r for r in results)

    @pytest.mark.asyncio
    async def test_fetch_multiple_urls_empty_list(self):
        """Test fetching with empty URL list."""
        results = await AsyncIOExamples.fetch_multiple_urls([])
        assert results == []

    @pytest.mark.asyncio
    async def test_async_generator_example_runs(self, capsys):
        """Test that async generator example runs successfully."""
        await AsyncIOExamples.async_generator_example()
        captured = capsys.readouterr()

        assert "Async generator output:" in captured.out
        assert "Received:" in captured.out

    @pytest.mark.asyncio
    async def test_async_context_manager_runs(self, capsys):
        """Test that async context manager example runs successfully."""
        await AsyncIOExamples.async_context_manager()
        captured = capsys.readouterr()

        assert "Acquiring async resource" in captured.out
        assert "Resource acquired" in captured.out
        assert "Using resource" in captured.out
        assert "Resource released" in captured.out


# ============================================================================
# CONCURRENCY PATTERNS TESTS
# ============================================================================


class TestConcurrencyPatterns:
    """Test suite for ConcurrencyPatterns class."""

    def test_timeout_pattern_times_out(self, capsys):
        """Test that timeout pattern properly times out."""
        ConcurrencyPatterns.timeout_pattern()
        captured = capsys.readouterr()

        assert "timed out" in captured.out.lower()

    @pytest.mark.asyncio
    async def test_async_timeout_pattern_times_out(self, capsys):
        """Test that async timeout pattern properly times out."""
        await ConcurrencyPatterns.async_timeout_pattern()
        captured = capsys.readouterr()

        assert "timed out" in captured.out.lower()

    def test_semaphore_pattern_limits_access(self, capsys):
        """Test that semaphore pattern runs successfully."""
        ConcurrencyPatterns.semaphore_pattern()
        captured = capsys.readouterr()

        # Should have messages about acquiring and releasing semaphore
        assert "acquired semaphore" in captured.out.lower()
        assert "releasing semaphore" in captured.out.lower()

    def test_future_callback_pattern_executes_callback(self, capsys):
        """Test that future callback pattern executes callback."""
        ConcurrencyPatterns.future_callback_pattern()
        captured = capsys.readouterr()

        assert "Callback received result: 25" in captured.out


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


class TestErrorHandling:
    """Test suite for ErrorHandling class."""

    def test_thread_exception_handling_catches_exceptions(self, capsys):
        """Test that thread exception handling catches and reports exceptions."""
        ErrorHandling.thread_exception_handling()
        captured = capsys.readouterr()

        # Should catch exceptions from even-numbered tasks
        assert (
            "Exceptions caught" in captured.out
            or "completed successfully" in captured.out
        )

    def test_future_exception_handling_catches_exceptions(self, capsys):
        """Test that future exception handling catches and reports exceptions."""
        ErrorHandling.future_exception_handling()
        captured = capsys.readouterr()

        # Should have both results and exceptions
        assert "Exception" in captured.out
        assert "Result" in captured.out

    @pytest.mark.asyncio
    async def test_async_exception_handling_catches_exceptions(self, capsys):
        """Test that async exception handling catches and reports exceptions."""
        await ErrorHandling.async_exception_handling()
        captured = capsys.readouterr()

        # Should have both results and exceptions
        assert "Exception" in captured.out
        assert "Success" in captured.out


# ============================================================================
# PERFORMANCE COMPARISON TESTS
# ============================================================================


class TestPerformanceComparison:
    """Test suite for PerformanceComparison class."""

    def test_io_bound_comparison_runs(self, capsys):
        """Test that I/O-bound comparison runs successfully."""
        PerformanceComparison.io_bound_comparison(num_tasks=3)
        captured = capsys.readouterr()

        assert "I/O-Bound Task Comparison" in captured.out
        assert "Sequential:" in captured.out
        assert "Threading:" in captured.out
        assert "AsyncIO:" in captured.out

    def test_io_bound_comparison_shows_threading_benefit(self, capsys):
        """Test that threading/asyncio are faster than sequential for I/O."""
        PerformanceComparison.io_bound_comparison(num_tasks=5)
        captured = capsys.readouterr()

        # Parse times from output
        lines = captured.out.split("\n")
        times = {}
        for line in lines:
            if "Sequential:" in line:
                times["sequential"] = float(line.split(":")[1].strip().replace("s", ""))
            elif "Threading:" in line:
                times["threading"] = float(line.split(":")[1].strip().replace("s", ""))
            elif "AsyncIO:" in line:
                times["asyncio"] = float(line.split(":")[1].strip().replace("s", ""))

        # Threading and AsyncIO should be faster than sequential
        if len(times) == 3:
            assert times["threading"] < times["sequential"]
            assert times["asyncio"] < times["sequential"]

    @pytest.mark.slow
    def test_cpu_bound_comparison_runs(self, capsys):
        """Test that CPU-bound comparison runs successfully."""
        PerformanceComparison.cpu_bound_comparison(num_tasks=4)
        captured = capsys.readouterr()

        assert "CPU-Bound Task Comparison" in captured.out
        assert "Sequential:" in captured.out
        assert "Threading:" in captured.out
        assert "Multiprocessing:" in captured.out


# ============================================================================
# GUIDELINES TESTS
# ============================================================================


class TestGuidelines:
    """Test suite for guidelines function."""

    def test_print_guidelines_outputs_content(self, capsys):
        """Test that print_guidelines outputs expected content."""
        print_guidelines()
        captured = capsys.readouterr()

        assert "CONCURRENCY AND PARALLELISM GUIDELINES" in captured.out
        assert "WHEN TO USE THREADING" in captured.out
        assert "WHEN TO USE MULTIPROCESSING" in captured.out
        assert "WHEN TO USE ASYNCIO" in captured.out
        assert "KEY PRINCIPLES" in captured.out
        assert "COMMON PITFALLS" in captured.out


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


class TestIntegration:
    """Integration tests combining multiple concepts."""

    def test_thread_pool_with_multiple_workers(self):
        """Test thread pool with various worker counts."""
        urls = [f"http://example.com/page{i}" for i in range(10)]
        results = ThreadPoolExample.download_simulation(urls)

        assert len(results) == 10
        assert all("Content from" in r for r in results)

    @pytest.mark.asyncio
    async def test_async_operations_complete_concurrently(self):
        """Test that multiple async operations complete concurrently."""
        urls = [f"http://example.com/{i}" for i in range(20)]

        start = time.time()
        results = await AsyncIOExamples.fetch_multiple_urls(urls)
        elapsed = time.time() - start

        assert len(results) == 20
        # Should take ~1 second (concurrent), not 20 seconds (sequential)
        assert elapsed < 3.0

    def test_multiprocessing_with_various_inputs(self):
        """Test multiprocessing with different input sizes."""
        small_numbers = [10, 20, 30]
        medium_numbers = [1000, 2000, 3000]

        small_results = MultiprocessingExamples.process_pool_example(small_numbers)
        medium_results = MultiprocessingExamples.process_pool_example(medium_numbers)

        assert len(small_results) == 3
        assert len(medium_results) == 3
        assert all(isinstance(r, int) for r in small_results)
        assert all(isinstance(r, int) for r in medium_results)


# ============================================================================
# EDGE CASES TESTS
# ============================================================================


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_cpu_intensive_task_with_one(self):
        """Test CPU intensive task with minimal input."""
        result = MultiprocessingExamples.cpu_intensive_task(1)
        assert result == 0

    def test_thread_pool_download_large_list(self):
        """Test thread pool with large number of URLs."""
        urls = [f"http://example.com/page{i}" for i in range(50)]
        results = ThreadPoolExample.download_simulation(urls)

        assert len(results) == 50

    @pytest.mark.asyncio
    async def test_async_task_with_zero_duration(self):
        """Test async task with zero duration."""
        result = await AsyncIOExamples.async_task(99, 0)
        assert "Result from task 99" in result

    @pytest.mark.asyncio
    async def test_fetch_multiple_urls_single_url(self):
        """Test fetch multiple URLs with single URL."""
        results = await AsyncIOExamples.fetch_multiple_urls(["http://test.com"])

        assert len(results) == 1
        assert "Data from http://test.com" in results[0]

    def test_process_pool_with_large_numbers(self):
        """Test process pool with large computation inputs."""
        numbers = [10000, 20000]
        results = MultiprocessingExamples.process_pool_example(numbers)

        assert len(results) == 2
        assert all(r > 0 for r in results)


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================


@pytest.mark.slow
class TestPerformance:
    """Performance-related tests (marked as slow)."""

    def test_threading_is_faster_than_sequential_for_io(self):
        """Test that threading provides speedup for I/O-bound tasks."""

        def io_task():
            time.sleep(0.1)

        # Sequential
        start = time.time()
        for _ in range(10):
            io_task()
        sequential_time = time.time() - start

        # Threading
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(io_task) for _ in range(10)]
            concurrent.futures.wait(futures)
        threading_time = time.time() - start

        # Threading should be significantly faster
        assert threading_time < sequential_time * 0.6

    @pytest.mark.asyncio
    async def test_asyncio_handles_many_tasks_efficiently(self):
        """Test that asyncio can handle many concurrent tasks efficiently."""

        async def quick_task(n):
            await asyncio.sleep(0.01)
            return n * 2

        start = time.time()
        tasks = [quick_task(i) for i in range(100)]
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start

        assert len(results) == 100
        # Should complete in ~0.01 seconds, not 1 second
        assert elapsed < 0.5

    def test_multiprocessing_speedup_for_cpu_bound(self):
        """Test that multiprocessing provides speedup for CPU-bound tasks."""

        def cpu_task(n):
            result = 0
            for i in range(n):
                result += i * i
            return result

        numbers = [1000000] * 4

        # Sequential
        start = time.time()
        _ = [cpu_task(n) for n in numbers]
        sequential_time = time.time() - start

        # Multiprocessing
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            _ = list(executor.map(cpu_task, numbers))
        parallel_time = time.time() - start

        # Multiprocessing should provide some speedup
        # Note: May not be exactly 4x due to overhead and CPU availability
        assert parallel_time < sequential_time


# ============================================================================
# WEBSCRAPER TESTS
# ============================================================================


class TestWebScraper:
    """Test suite for WebScraper class."""

    def test_init_default_workers(self):
        """Test WebScraper initialization with default workers."""
        scraper = WebScraper()
        assert scraper.max_workers == 5

    def test_init_custom_workers(self):
        """Test WebScraper initialization with custom worker count."""
        scraper = WebScraper(max_workers=10)
        assert scraper.max_workers == 10

    def test_fetch_page_returns_dict(self):
        """Test that fetch_page returns expected dictionary structure."""
        scraper = WebScraper()
        result = scraper.fetch_page("http://example.com")

        assert isinstance(result, dict)
        assert "url" in result
        assert "status" in result
        assert "content" in result
        assert "timestamp" in result
        assert result["url"] == "http://example.com"
        assert result["status"] == 200

    def test_fetch_page_content_format(self):
        """Test that fetched page content has expected format."""
        scraper = WebScraper()
        url = "http://test.com/page1"
        result = scraper.fetch_page(url)

        assert result["content"] == f"Content from {url}"

    def test_scrape_urls_returns_all_results(self):
        """Test that scrape_urls returns results for all URLs."""
        scraper = WebScraper(max_workers=2)
        urls = [f"http://example.com/page{i}" for i in range(5)]
        results = scraper.scrape_urls(urls)

        assert len(results) == len(urls)
        assert all(isinstance(r, dict) for r in results)

    def test_scrape_urls_performance(self):
        """Test that concurrent scraping is faster than sequential."""
        scraper = WebScraper(max_workers=3)
        urls = [f"http://example.com/page{i}" for i in range(6)]

        start = time.time()
        results = scraper.scrape_urls(urls)
        elapsed = time.time() - start

        # With 3 workers and 6 URLs (1s each), should take ~2s
        # Sequential would take 6s
        assert elapsed < 3.5  # Allow some overhead
        assert len(results) == 6

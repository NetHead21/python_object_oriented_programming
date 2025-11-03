"""Practical Concurrency Examples - Real-World Use Cases.

This module contains practical, real-world examples of using concurrency
and parallelism in Python applications.

Examples include:
- Web scraping with concurrent requests
- Parallel data processing
- Async web server patterns
- Batch processing with multiprocessing
- Real-time data streaming
"""

import asyncio
import concurrent.futures
import time
import threading
import multiprocessing
from typing import List, Dict, Any, Callable
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# EXAMPLE 1: WEB SCRAPING WITH CONCURRENT REQUESTS
# ============================================================================


class WebScraper:
    """Concurrent web scraper using ThreadPoolExecutor.

    Demonstrates efficient web scraping by making multiple HTTP requests
    concurrently, reducing total scraping time.
    """

    def __init__(self, max_workers: int = 5):
        """Initialize the web scraper.

        Args:
            max_workers: Maximum number of concurrent requests
        """
        self.max_workers = max_workers

    def fetch_page(self, url: str) -> Dict[str, Any]:
        """Simulate fetching a web page.

        In a real application, you would use requests or aiohttp library.

        Args:
            url: URL to fetch

        Returns:
            Dictionary containing URL and simulated content
        """
        print(f"Fetching: {url}")
        time.sleep(1)  # Simulate network delay

        return {
            "url": url,
            "status": 200,
            "content": f"Content from {url}",
            "timestamp": datetime.now().isoformat(),
        }

    def scrape_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Scrape multiple URLs concurrently.

        Args:
            urls: List of URLs to scrape

        Returns:
            List of results from all URLs

        Example:
            >>> scraper = WebScraper(max_workers=3)
            >>> urls = [f"http://example.com/page{i}" for i in range(10)]
            >>> results = scraper.scrape_urls(urls)
            >>> len(results)
            10
        """

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            results = list(executor.map(self.fetch_page, urls))

        elapsed = time.time() - start_time
        print(f"Scraped {len(urls)} URLs in {elapsed:.2f} seconds")

        return results

    def scrape_with_error_handling(self, urls: List[str]) -> Dict[str, Any]:
        """Scrape URLs with comprehensive error handling.

        Args:
            urls: List of URLs to scrape

        Returns:
            Dictionary with successful results and errors
        """
        successful = []
        failed = []

        def safe_fetch(url: str) -> tuple[bool, Any]:
            """Fetch with exception handling."""
            try:
                result = self.fetch_page(url)
                return True, result
            except Exception as e:
                return False, {"url": url, "error": str(e)}

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            futures = {executor.submit(safe_fetch, url): url for url in urls}

            for future in concurrent.futures.as_completed(futures):
                success, result = future.result()
                if success:
                    successful.append(result)
                else:
                    failed.append(result)

        return {
            "successful": successful,
            "failed": failed,
            "total": len(urls),
            "success_rate": len(successful) / len(urls) if urls else 0,
        }


# ============================================================================
# EXAMPLE 2: PARALLEL DATA PROCESSING
# ============================================================================


@dataclass
class DataRecord:
    """Represents a data record to be processed."""

    id: int
    value: float
    category: str


class DataProcessor:
    """Parallel data processor using multiprocessing.

    Demonstrates CPU-intensive data processing using multiple processes
    to achieve true parallelism.
    """

    @staticmethod
    def process_record(record: DataRecord) -> DataRecord:
        """Process a single data record (CPU-intensive operation).

        Args:
            record: Record to process

        Returns:
            Processed record
        """
        # Simulate CPU-intensive computation
        result = 0
        for i in range(1000000):
            result += i * record.value

        # Transform the record
        return DataRecord(
            id=record.id, value=record.value * 2, category=record.category.upper()
        )

    @staticmethod
    def process_batch_parallel(
        records: List[DataRecord], num_workers: int = None
    ) -> List[DataRecord]:
        """Process records in parallel using multiprocessing.

        Args:
            records: List of records to process
            num_workers: Number of worker processes (default: CPU count)

        Returns:
            List of processed records

        Example:
            >>> records = [DataRecord(i, i*1.5, "type_a") for i in range(100)]
            >>> processed = DataProcessor.process_batch_parallel(records)
            >>> len(processed) == len(records)
            True
        """
        if num_workers is None:
            num_workers = multiprocessing.cpu_count()

        start_time = time.time()

        with concurrent.futures.ProcessPoolExecutor(
            max_workers=num_workers
        ) as executor:
            results = list(executor.map(DataProcessor.process_record, records))

        elapsed = time.time() - start_time
        print(
            f"Processed {len(records)} records in {elapsed:.2f}s using {num_workers} workers"
        )

        return results

    @staticmethod
    def process_in_chunks(
        records: List[DataRecord], chunk_size: int = 100
    ) -> List[DataRecord]:
        """Process records in chunks for better memory efficiency.

        Args:
            records: List of records to process
            chunk_size: Size of each chunk

        Returns:
            List of all processed records
        """

        def process_chunk(chunk: List[DataRecord]) -> List[DataRecord]:
            """Process a chunk of records."""
            return [DataProcessor.process_record(r) for r in chunk]

        # Split into chunks
        chunks = [
            records[i : i + chunk_size] for i in range(0, len(records), chunk_size)
        ]

        # Process chunks in parallel
        with concurrent.futures.ProcessPoolExecutor() as executor:
            processed_chunks = list(executor.map(process_chunk, chunks))

        # Flatten results
        return [record for chunk in processed_chunks for record in chunk]


# ============================================================================
# EXAMPLE 3: ASYNC WEB API CLIENT
# ============================================================================


class AsyncAPIClient:
    """Asynchronous API client using asyncio.

    Demonstrates efficient API interaction using async/await for
    handling many concurrent API requests.
    """

    def __init__(self, base_url: str, rate_limit: int = 10):
        """Initialize the API client.

        Args:
            base_url: Base URL for the API
            rate_limit: Maximum concurrent requests
        """
        self.base_url = base_url
        self.semaphore = asyncio.Semaphore(rate_limit)

    async def fetch_resource(self, resource_id: int) -> Dict[str, Any]:
        """Fetch a single resource from the API.

        Args:
            resource_id: ID of the resource to fetch

        Returns:
            Resource data
        """

        async with self.semaphore:  # Rate limiting
            print(f"Fetching resource {resource_id}")
            await asyncio.sleep(0.5)  # Simulate API call

            return {
                "id": resource_id,
                "data": f"Resource data for {resource_id}",
                "timestamp": datetime.now().isoformat(),
            }

    async def fetch_multiple_resources(
        self, resource_ids: List[int]
    ) -> List[Dict[str, Any]]:
        """Fetch multiple resources concurrently.

        Args:
            resource_ids: List of resource IDs to fetch

        Returns:
            List of resource data

        Example:
            >>> client = AsyncAPIClient("https://api.example.com")
            >>> ids = list(range(20))
            >>> results = asyncio.run(client.fetch_multiple_resources(ids))
            >>> len(results)
            20
        """

        start_time = time.time()

        # Create tasks for all requests
        tasks = [self.fetch_resource(rid) for rid in resource_ids]

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks)

        elapsed = time.time() - start_time
        print(f"Fetched {len(resource_ids)} resources in {elapsed:.2f}s")

        return results

    async def fetch_with_retry(
        self, resource_id: int, max_retries: int = 3
    ) -> Dict[str, Any]:
        """Fetch resource with automatic retry on failure.

        Args:
            resource_id: ID of the resource
            max_retries: Maximum number of retry attempts

        Returns:
            Resource data

        Raises:
            Exception: If all retries fail
        """

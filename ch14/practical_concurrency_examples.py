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

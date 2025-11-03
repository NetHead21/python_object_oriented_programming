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

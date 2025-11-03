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

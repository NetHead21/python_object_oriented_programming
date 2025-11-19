"""Comprehensive tests for practical_concurrency_examples module."""

import asyncio
import pytest
from unittest.mock import Mock, patch
import time
from pathlib import Path
import sys


# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from practical_concurrency_examples import (
    WebScraper,
    DataRecord,
    DataProcessor,
    AsyncAPIClient,
    StreamProcessor,
    FileProcessor,
    AsyncBatchProcessor,
)


# Module-level functions for pickling (needed for multiprocessing)
def simple_transform(record):
    """Simple transformation function for testing."""
    return DataRecord(record.id, record.value * 2, record.category.upper())


def word_count_processor(content):
    """Count words in content."""
    return len(content.split())


def simple_content_processor(content):
    """Simple processor that returns content length."""
    return len(content)


def char_count_processor(content):
    """Count characters in content."""
    return len(content)


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
        """Test WebScraper initialization with custom workers."""
        scraper = WebScraper(max_workers=10)
        assert scraper.max_workers == 10

    def test_fetch_page_returns_dict(self):
        """Test that fetch_page returns a dictionary."""
        scraper = WebScraper()
        result = scraper.fetch_page("http://example.com")

        assert isinstance(result, dict)
        assert "url" in result
        assert "status" in result
        assert "content" in result
        assert "timestamp" in result

    def test_fetch_page_content_format(self):
        """Test that fetch_page returns correct content format."""
        scraper = WebScraper()
        url = "http://test.com"
        result = scraper.fetch_page(url)

        assert result["url"] == url
        assert result["status"] == 200
        assert f"Content from {url}" in result["content"]

    def test_scrape_urls_returns_all_results(self):
        """Test that scrape_urls returns results for all URLs."""
        scraper = WebScraper(max_workers=2)
        urls = [f"http://example.com/page{i}" for i in range(5)]

        results = scraper.scrape_urls(urls)

        assert len(results) == len(urls)
        assert all(isinstance(r, dict) for r in results)

    def test_scrape_urls_performance(self):
        """Test that scraping is faster with concurrency."""
        scraper = WebScraper(max_workers=5)
        urls = [f"http://example.com/page{i}" for i in range(5)]

        start = time.time()
        results = scraper.scrape_urls(urls)
        elapsed = time.time() - start

        # With 5 workers and 5 URLs taking 1 second each, should complete in ~1-2 seconds
        # not 5 seconds (sequential)
        assert elapsed < 3.0
        assert len(results) == 5

    def test_scrape_urls_empty_list(self):
        """Test scraping empty URL list."""
        scraper = WebScraper()
        results = scraper.scrape_urls([])
        assert results == []

    def test_scrape_urls_single_url(self):
        """Test scraping single URL."""
        scraper = WebScraper()
        results = scraper.scrape_urls(["http://single.com"])

        assert len(results) == 1
        assert results[0]["url"] == "http://single.com"

    def test_scrape_with_error_handling_all_success(self):
        """Test error handling with all successful requests."""
        scraper = WebScraper()
        urls = [f"http://example.com/page{i}" for i in range(3)]

        result = scraper.scrape_with_error_handling(urls)

        assert result["total"] == 3
        assert len(result["successful"]) == 3
        assert len(result["failed"]) == 0
        assert result["success_rate"] == 1.0

    def test_scrape_with_error_handling_structure(self):
        """Test that error handling returns correct structure."""
        scraper = WebScraper()
        result = scraper.scrape_with_error_handling(["http://test.com"])

        assert "successful" in result
        assert "failed" in result
        assert "total" in result
        assert "success_rate" in result

    def test_scrape_with_error_handling_empty_urls(self):
        """Test error handling with empty URL list."""
        scraper = WebScraper()
        result = scraper.scrape_with_error_handling([])

        assert result["total"] == 0
        assert result["success_rate"] == 0

    def test_scrape_with_error_handling_partial_failure(self):
        """Test error handling when some requests succeed."""
        scraper = WebScraper()

        # Mock fetch_page to fail on specific URLs
        original_fetch = scraper.fetch_page

        def mock_fetch(url):
            if "fail" in url:
                raise Exception("Simulated error")
            return original_fetch(url)

        scraper.fetch_page = mock_fetch

        urls = ["http://success.com", "http://fail.com", "http://success2.com"]
        result = scraper.scrape_with_error_handling(urls)

        assert result["total"] == 3
        assert len(result["successful"]) == 2
        assert len(result["failed"]) == 1


# ============================================================================
# DATARECORD AND DATAPROCESSOR TESTS
# ============================================================================


class TestDataRecord:
    """Test suite for DataRecord dataclass."""

    def test_datarecord_creation(self):
        """Test creating a DataRecord instance."""
        record = DataRecord(1, 10.5, "test")

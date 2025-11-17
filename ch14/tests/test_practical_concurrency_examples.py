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

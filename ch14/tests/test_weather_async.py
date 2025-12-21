import asyncio
import re
import sys
from pathlib import Path

import pytest
from pytest_httpx import HTTPXMock

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import weather_async

# ============================================================================
# Zone Tests
# ============================================================================


class TestZone:
    """Comprehensive tests for the Zone class."""

    def test_zone_basic_creation(self):
        """Test basic Zone creation with valid data."""

        zone = weather_async.Zone("Eastern Bay", "ANZ540", "073540")
        assert zone.zone_name == "Eastern Bay"
        assert zone.zone_code == "ANZ540"
        assert zone.same_code == "073540"

    def test_zone_forecast_url_generation(self):
        """Test forecast URL generation with proper formatting."""

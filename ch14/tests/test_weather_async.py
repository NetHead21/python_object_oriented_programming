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

        zone = weather_async.Zone("Eastern Bay", "ANZ540", "073540")
        expected_url = (
            "https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/an/anz540.txt"
        )
        assert zone.forecast_url == expected_url

    def test_zone_forecast_url_lowercase_conversion(self):
        """Test that zone code is properly lowercased in URL."""

        zone = weather_async.Zone("Test Zone", "ANZ123", "073123")
        assert "anz123.txt" in zone.forecast_url
        assert "ANZ123" not in zone.forecast_url

    def test_zone_immutability(self):
        """Test that Zone is immutable (NamedTuple behavior)."""

        zone = weather_async.Zone("Test", "ANZ123", "073123")
        with pytest.raises(AttributeError):
            zone.zone_name = "Modified"

    def test_zone_tuple_unpacking(self):
        """Test Zone can be unpacked like a tuple."""

        zone = weather_async.Zone("Test Zone", "ANZ123", "073123")
        name, code, same = zone
        assert name == "Test Zone"
        assert code == "ANZ123"
        assert same == "073123"

    def test_zone_indexing(self):
        """Test Zone supports index access."""

        zone = weather_async.Zone("Test Zone", "ANZ123", "073123")
        assert zone[0] == "Test Zone"
        assert zone[1] == "ANZ123"
        assert zone[2] == "073123"

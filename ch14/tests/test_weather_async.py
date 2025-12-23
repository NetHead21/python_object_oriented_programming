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

    def test_zone_equality(self):
        """Test Zone equality comparison."""

        zone1 = weather_async.Zone("Test", "ANZ123", "073123")
        zone2 = weather_async.Zone("Test", "ANZ123", "073123")
        zone3 = weather_async.Zone("Test", "ANZ456", "073456")
        assert zone1 == zone2
        assert zone1 != zone3

    def test_zone_hashable(self):
        """Test Zone can be used in sets and as dict keys."""

        zone1 = weather_async.Zone("Test1", "ANZ123", "073123")
        zone2 = weather_async.Zone("Test2", "ANZ456", "073456")
        zone_set = {zone1, zone2}
        assert len(zone_set) == 2
        zone_dict = {zone1: "value1", zone2: "value2"}
        assert zone_dict[zone1] == "value1"

    def test_zone_with_special_characters(self):
        """Test Zone with special characters in name."""

        zone = weather_async.Zone("Chesapeake Bay - North, MD/VA", "ANZ123", "073123")
        assert zone.zone_name == "Chesapeake Bay - North, MD/VA"

    def test_zone_with_empty_name(self):
        """Test Zone with empty name (edge case)."""
        zone = weather_async.Zone("", "ANZ123", "073123")
        assert zone.zone_name == ""
        assert zone.forecast_url.endswith("anz123.txt")


# ============================================================================
# MarineWX Tests
# ============================================================================


class TestMarineWX:
    """Comprehensive tests for the MarineWX class."""

    @pytest.fixture
    def sample_zone(self):
        """Provide a sample zone for testing."""
        return weather_async.Zone("Eastern Bay", "ANZ540", "073540")

    @pytest.fixture
    def marine_wx(self, sample_zone):
        """Provide a MarineWX instance for testing."""
        return weather_async.MarineWX(sample_zone)

    def test_marinewx_initialization(self, sample_zone):
        """Test MarineWX initialization."""
        wx = weather_async.MarineWX(sample_zone)
        assert wx.zone == sample_zone
        assert wx.doc == ""

    def test_marinewx_advisory_pattern(self):
        """Test the advisory regex pattern."""

        pattern = weather_async.MarineWX.advisory_pat
        assert isinstance(pattern, re.Pattern)

        # Test pattern matches advisory format
        text = "\n...SMALL CRAFT ADVISORY...\n"
        match = pattern.search(text)
        assert match is not None

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

        # Pattern captures content up to (but not including) final ..
        assert match.group(1) == "SMALL CRAFT ADVISORY."

    @pytest.mark.asyncio
    async def test_marinewx_run_success(self, marine_wx, httpx_mock: HTTPXMock):
        """Test successful forecast fetch."""
        httpx_mock.add_response(
            method="GET",
            url=marine_wx.zone.forecast_url,
            text="Heading\n...SMALL CRAFT ADVISORY...\n.DAY...details.\n",
        )
        await marine_wx.run()
        assert marine_wx.doc == "Heading\n...SMALL CRAFT ADVISORY...\n.DAY...details.\n"
        assert marine_wx.advisory == "SMALL CRAFT ADVISORY."

    @pytest.mark.asyncio
    async def test_marinewx_run_updates_doc(self, marine_wx, httpx_mock: HTTPXMock):
        """Test that run() updates the doc attribute."""
        forecast_text = "Test forecast document"
        httpx_mock.add_response(
            method="GET", url=marine_wx.zone.forecast_url, text=forecast_text
        )
        assert marine_wx.doc == ""
        await marine_wx.run()
        assert marine_wx.doc == forecast_text

    def test_marinewx_advisory_extraction_simple(self, marine_wx):
        """Test advisory extraction with simple advisory."""
        marine_wx.doc = "Forecast\n...SMALL CRAFT ADVISORY...\nDetails"
        assert marine_wx.advisory == "SMALL CRAFT ADVISORY."

    def test_marinewx_advisory_extraction_multiline(self, marine_wx):
        """Test advisory extraction with multiline advisory."""
        marine_wx.doc = (
            "Forecast\n...SMALL CRAFT ADVISORY IN EFFECT\n"
            "FROM 6 PM THIS EVENING TO 6 AM EST SATURDAY...\nDetails"
        )
        expected = "SMALL CRAFT ADVISORY IN EFFECT FROM 6 PM THIS EVENING TO 6 AM EST SATURDAY."
        assert marine_wx.advisory == expected

    def test_marinewx_advisory_no_advisory(self, marine_wx):
        """Test advisory extraction when no advisory present."""
        marine_wx.doc = "Forecast with no advisory section"
        assert marine_wx.advisory == ""

    def test_marinewx_advisory_empty_doc(self, marine_wx):
        """Test advisory extraction with empty doc."""
        marine_wx.doc = ""
        assert marine_wx.advisory == ""

    def test_marinewx_advisory_multiple_advisories(self, marine_wx):
        """Test advisory extraction with multiple advisories (returns first)."""
        marine_wx.doc = (
            "Forecast\n...SMALL CRAFT ADVISORY...\nMiddle\n...GALE WARNING...\nEnd"
        )
        # Should return first match
        assert marine_wx.advisory == "SMALL CRAFT ADVISORY."

    def test_marinewx_advisory_with_dots_inside(self, marine_wx):
        """Test advisory with dots inside the text."""
        marine_wx.doc = "Forecast\n...ADVISORY...DETAILS...CONTINUE...\nEnd"
        assert "ADVISORY...DETAILS...CONTINUE" in marine_wx.advisory

    def test_marinewx_repr_with_advisory(self, marine_wx):
        """Test __repr__ with advisory present."""
        marine_wx.doc = "Forecast\n...SMALL CRAFT ADVISORY...\nDetails"
        expected = "Eastern Bay SMALL CRAFT ADVISORY."
        assert repr(marine_wx) == expected

    def test_marinewx_repr_without_advisory(self, marine_wx):
        """Test __repr__ without advisory present."""
        marine_wx.doc = "Forecast with no advisory"
        assert repr(marine_wx) == "Eastern Bay "

    @pytest.mark.asyncio
    async def test_marinewx_concurrent_runs(self, sample_zone, httpx_mock: HTTPXMock):
        """Test multiple concurrent MarineWX runs."""
        zones = [
            weather_async.Zone(f"Zone {i}", f"ANZ{i:03d}", f"073{i:03d}")
            for i in range(5)
        ]
        forecasts = [weather_async.MarineWX(z) for z in zones]

        # Mock all responses
        for i, wx in enumerate(forecasts):
            httpx_mock.add_response(
                method="GET",
                url=wx.zone.forecast_url,
                text=f"Forecast {i}\n...ADVISORY {i}...\n",
            )

        # Run all concurrently
        await asyncio.gather(*(f.run() for f in forecasts))

        # Verify all completed
        for i, wx in enumerate(forecasts):
            assert f"Forecast {i}" in wx.doc
            assert wx.advisory == f"ADVISORY {i}."


# ============================================================================
# Edge Case Tests
# ============================================================================


class TestEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.mark.asyncio
    async def test_empty_response(self, httpx_mock: HTTPXMock):
        """Test handling of empty response."""
        zone = weather_async.Zone("Test", "ANZ123", "073123")
        wx = weather_async.MarineWX(zone)
        httpx_mock.add_response(method="GET", url=zone.forecast_url, text="")
        await wx.run()
        assert wx.doc == ""
        assert wx.advisory == ""

    @pytest.mark.asyncio
    async def test_very_large_response(self, httpx_mock: HTTPXMock):
        """Test handling of very large response."""
        zone = weather_async.Zone("Test", "ANZ123", "073123")
        wx = weather_async.MarineWX(zone)
        large_text = "X" * 1000000  # 1MB of data
        httpx_mock.add_response(method="GET", url=zone.forecast_url, text=large_text)
        await wx.run()
        assert len(wx.doc) == 1000000

    @pytest.mark.asyncio
    async def test_special_characters_in_response(self, httpx_mock: HTTPXMock):
        """Test handling of special characters in response."""
        zone = weather_async.Zone("Test", "ANZ123", "073123")
        wx = weather_async.MarineWX(zone)
        special_text = "Forecast\n...ADVISORY™ ©® €¥£...\n"
        httpx_mock.add_response(method="GET", url=zone.forecast_url, text=special_text)
        await wx.run()
        assert "™ ©® €¥£" in wx.advisory

    @pytest.mark.asyncio
    async def test_unicode_in_response(self, httpx_mock: HTTPXMock):
        """Test handling of Unicode characters in response."""
        zone = weather_async.Zone("Test", "ANZ123", "073123")
        wx = weather_async.MarineWX(zone)
        unicode_text = "Forecast\n...ADVISORY 中文 日本語 한글...\n"
        httpx_mock.add_response(method="GET", url=zone.forecast_url, text=unicode_text)
        await wx.run()
        assert "中文 日本語 한글" in wx.advisory

    def test_advisory_pattern_with_newlines(self):
        """Test advisory pattern handles various newline formats."""
        wx = weather_async.MarineWX(weather_async.Zone("Test", "ANZ123", "073123"))
        # Unix newlines
        wx.doc = "Forecast\n...ADVISORY...\nDetails"
        assert wx.advisory == "ADVISORY."

        # Windows newlines - pattern requires Unix-style \n, so won't match
        wx.doc = "Forecast\r\n...ADVISORY...\r\nDetails"
        # Pattern uses \n not \r\n, so no match with pure Windows newlines
        assert wx.advisory == ""

    def test_advisory_with_only_dots(self):
        """Test advisory pattern doesn't match just dots."""
        wx = weather_async.MarineWX(weather_async.Zone("Test", "ANZ123", "073123"))
        wx.doc = "Forecast\n...\nDetails"
        assert wx.advisory == ""

    def test_zone_list_exists(self):
        """Test that ZONES list is properly defined."""
        assert hasattr(weather_async, "ZONES")
        assert isinstance(weather_async.ZONES, list)
        assert len(weather_async.ZONES) > 0

    def test_zone_list_all_valid(self):
        """Test that all zones in ZONES list are valid."""
        for zone in weather_async.ZONES:
            assert isinstance(zone, weather_async.Zone)
            assert zone.zone_name
            assert zone.zone_code
            assert zone.same_code
            assert zone.forecast_url.startswith("https://")

    @pytest.mark.asyncio
    async def test_marinewx_multiple_calls_to_run(self, httpx_mock: HTTPXMock):
        """Test calling run() multiple times updates doc."""
        zone = weather_async.Zone("Test", "ANZ123", "073123")
        wx = weather_async.MarineWX(zone)

        # First call
        httpx_mock.add_response(
            method="GET", url=zone.forecast_url, text="First forecast"
        )
        await wx.run()
        assert wx.doc == "First forecast"

        # Second call
        httpx_mock.add_response(
            method="GET", url=zone.forecast_url, text="Second forecast"
        )
        await wx.run()
        assert wx.doc == "Second forecast"


# ============================================================================
# Integration Tests
# ============================================================================


class TestIntegration:
    """Integration tests for the complete workflow."""

    @pytest.mark.asyncio
    async def test_complete_workflow(self, httpx_mock: HTTPXMock):
        """Test complete workflow from zone creation to result."""
        # Create zone
        zone = weather_async.Zone("Test Zone", "ANZ123", "073123")

        # Create MarineWX
        wx = weather_async.MarineWX(zone)

        # Mock response
        forecast = """
        FZUS51 KLWX 221234
        MARINE WEATHER STATEMENT
        ...SMALL CRAFT ADVISORY IN EFFECT FROM 6 PM THIS EVENING TO 6 AM EST SATURDAY...
        .TONIGHT...Southwest winds 15 to 20 kt.
        $$
        """

        httpx_mock.add_response(method="GET", url=zone.forecast_url, text=forecast)

        # Run fetch
        await wx.run()

        # Verify results
        assert wx.doc == forecast
        assert "SMALL CRAFT ADVISORY" in wx.advisory
        assert "6 PM THIS EVENING TO 6 AM EST SATURDAY" in wx.advisory
        result = repr(wx)
        assert "Test Zone" in result
        assert "SMALL CRAFT ADVISORY" in result

    @pytest.mark.asyncio
    async def test_gather_multiple_forecasts(self, httpx_mock: HTTPXMock):
        """Test gathering multiple forecasts concurrently."""
        zones = [
            weather_async.Zone(f"Zone {i}", f"ANZ{i:03d}", f"073{i:03d}")
            for i in range(3)
        ]
        forecasts = [weather_async.MarineWX(z) for z in zones]

        # Mock all responses
        for i, wx in enumerate(forecasts):
            httpx_mock.add_response(
                method="GET",
                url=wx.zone.forecast_url,
                text=f"Forecast {i}\n...ADVISORY {i}...\n",
            )

        # Gather using asyncio
        await asyncio.gather(*(f.run() for f in forecasts))

        # Verify all completed
        for i, wx in enumerate(forecasts):
            assert wx.advisory == f"ADVISORY {i}."

    @pytest.mark.asyncio
    async def test_realistic_forecast_format(self, httpx_mock: HTTPXMock):
        """Test with realistic NWS forecast format."""
        zone = weather_async.Zone("Eastern Bay", "ANZ540", "073540")
        wx = weather_async.MarineWX(zone)

        realistic_forecast = """
        FZUS51 KLWX 221234
        MARINE WEATHER STATEMENT
        NATIONAL WEATHER SERVICE STERLING VA
        734 AM EST SUN DEC 22 2025

        ...SMALL CRAFT ADVISORY IN EFFECT FROM 6 PM THIS EVENING TO
        6 AM EST SATURDAY...

        ANZ540-221500-
        EASTERN BAY-
        734 AM EST SUN DEC 22 2025

        .TODAY...Southwest winds 10 to 15 kt. Seas 2 to 3 ft.
        .TONIGHT...Southwest winds 15 to 20 kt with gusts up to 25 kt. 
        Seas 3 to 4 ft.
        .MONDAY...West winds 20 to 25 kt with gusts up to 30 kt. Seas 
        4 to 5 ft.

        $$
        """

        httpx_mock.add_response(
            method="GET", url=zone.forecast_url, text=realistic_forecast
        )

        await wx.run()

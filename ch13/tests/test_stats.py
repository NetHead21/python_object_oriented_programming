import sys
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.stats import StatsList
import pytest


# =============================================================================
# Tests for mean()
# =============================================================================


class TestMean:
    """Test cases for the mean() method."""

    def test_mean_simple_integers(self):
        """Test mean with simple integer values."""
        data = StatsList([1, 2, 3, 4, 5])
        assert data.mean() == 3.0

    def test_mean_with_none_values(self):
        """Test mean calculation with some None values."""
        data = StatsList([1, 2, None, 4, None])
        assert data.mean() == pytest.approx(2.3333333, rel=1e-5)

    def test_mean_all_none_raises_error(self):
        """Test that all None values raises ValueError."""
        data = StatsList([None, None, None])
        with pytest.raises(ValueError, match="Cannot compute mean of empty sequence"):
            data.mean()

    def test_mean_empty_list_raises_error(self):
        """Test that empty list raises ValueError."""
        data = StatsList([])
        with pytest.raises(ValueError, match="Cannot compute mean of empty sequence"):
            data.mean()

    def test_mean_floats(self):
        """Test mean with floating point numbers."""
        data = StatsList([1.5, 2.5, 3.5])
        assert data.mean() == 2.5

    def test_mean_negative_numbers(self):
        """Test mean with negative numbers."""
        data = StatsList([-1, -2, -3, -4, -5])
        assert data.mean() == -3.0

    def test_mean_mixed_positive_negative(self):
        """Test mean with mixed positive and negative numbers."""
        data = StatsList([-2, -1, 0, 1, 2])
        assert data.mean() == 0.0

    def test_mean_single_value(self):
        """Test mean with a single value."""
        data = StatsList([42])
        assert data.mean() == 42.0


# =============================================================================
# Tests for median()
# =============================================================================


class TestMedian:
    """Test cases for the median() method."""

    def test_median_odd_count(self):
        """Test median with odd number of elements."""
        data = StatsList([1, 2, 3, 4, 5])
        assert data.median() == 3

    def test_median_even_count(self):
        """Test median with even number of elements."""
        data = StatsList([1, 2, 3, 4])
        assert data.median() == 2.5

    def test_median_with_none(self):
        """Test median calculation ignores None values."""
        # Note: median() expects pre-sorted data as per docstring
        data = StatsList([1, None, 3, None, 5])
        assert data.median() == 3

    def test_median_single_value(self):
        """Test median with single value."""
        data = StatsList([42])
        assert data.median() == 42

    def test_median_all_none_raises_error(self):
        """Test that all None values raises ValueError."""
        data = StatsList([None, None])
        with pytest.raises(ValueError, match="Cannot compute median of empty sequence"):
            data.median()

    def test_median_empty_raises_error(self):
        """Test that empty list raises ValueError."""
        data = StatsList([])
        with pytest.raises(ValueError, match="Cannot compute median of empty sequence"):
            data.median()

    def test_median_two_values(self):
        """Test median with two values."""
        data = StatsList([1, 3])
        assert data.median() == 2.0


# =============================================================================
# Tests for mode()
# =============================================================================


class TestMode:
    """Test cases for the mode() method."""

    def test_mode_single_mode(self):
        """Test mode with a single most frequent value."""
        data = StatsList([1, 2, 2, 3, 4])
        assert data.mode() == [2]

    def test_mode_bimodal(self):
        """Test mode with two values having same frequency."""
        data = StatsList([1, 1, 2, 2, 3])
        result = sorted(data.mode())
        assert result == [1, 2]

    def test_mode_uniform_distribution(self):
        """Test mode when all values appear once."""
        data = StatsList([1, 2, 3, 4])
        result = sorted(data.mode())
        assert result == [1, 2, 3, 4]

    def test_mode_with_none(self):
        """Test mode with None values."""
        data = StatsList([1, None, 2, 2, None, 3])
        assert data.mode() == [2]

    def test_mode_all_none(self):
        """Test mode with all None values."""
        data = StatsList([None, None])
        assert data.mode() == []

    def test_mode_empty_list(self):
        """Test mode with empty list."""
        data = StatsList([])
        assert data.mode() == []

    def test_mode_all_same(self):
        """Test mode when all values are the same."""
        data = StatsList([5, 5, 5, 5])
        assert data.mode() == [5]


# =============================================================================
# Tests for variance()
# =============================================================================


class TestVariance:
    """Test cases for the variance() method."""

    def test_variance_simple(self):
        """Test variance with simple values."""
        data = StatsList([1, 2, 3, 4, 5])
        assert data.variance() == 2.0

    def test_variance_all_same(self):
        """Test variance when all values are identical."""
        data = StatsList([10, 10, 10, 10])
        assert data.variance() == 0.0

    def test_variance_with_none(self):
        """Test variance with None values."""
        data = StatsList([1, None, 5, None, 9])
        assert data.variance() == pytest.approx(10.666666, rel=1e-5)

    def test_variance_all_none_raises_error(self):
        """Test that all None values raises ValueError."""
        data = StatsList([None, None])
        with pytest.raises(
            ValueError, match="Cannot compute variance of empty sequence"
        ):
            data.variance()

    def test_variance_empty_raises_error(self):
        """Test that empty list raises ValueError."""
        data = StatsList([])
        with pytest.raises(
            ValueError, match="Cannot compute variance of empty sequence"
        ):
            data.variance()

    def test_variance_single_value(self):
        """Test variance with single value (should be 0)."""
        data = StatsList([5])
        assert data.variance() == 0.0

    def test_variance_negative_values(self):
        """Test variance with negative values."""
        data = StatsList([-2, -1, 0, 1, 2])
        # Variance of [-2, -1, 0, 1, 2]: mean=0, sum of squared deviations = 4+1+0+1+4 = 10, variance = 10/5 = 2.5
        assert data.variance() == 2.5


# =============================================================================
# Tests for stddev()
# =============================================================================


class TestStddev:
    """Test cases for the stddev() method."""

    def test_stddev_simple(self):
        """Test standard deviation with simple values."""
        data = StatsList([1, 2, 3, 4, 5])
        assert round(data.stddev(), 4) == 1.4142

    def test_stddev_all_same(self):
        """Test standard deviation when all values are identical."""
        data = StatsList([10, 10, 10, 10])
        assert data.stddev() == 0.0

    def test_stddev_with_none(self):
        """Test standard deviation with None values."""
        data = StatsList([1, None, 5, None, 9])
        assert round(data.stddev(), 4) == 3.2660

    def test_stddev_all_none_raises_error(self):
        """Test that all None values raises ValueError."""
        data = StatsList([None])
        with pytest.raises(ValueError):
            data.stddev()

    def test_stddev_empty_raises_error(self):
        """Test that empty list raises ValueError."""
        data = StatsList([])
        with pytest.raises(ValueError):
            data.stddev()

    def test_stddev_is_sqrt_of_variance(self):
        """Test that stddev is the square root of variance."""
        data = StatsList([1, 2, 3, 4, 5])
        import math

        assert data.stddev() == pytest.approx(math.sqrt(data.variance()))


# =============================================================================
# Tests for quantile()
# =============================================================================


class TestQuantile:
    """Test cases for the quantile() method."""

    def test_quantile_median(self):
        """Test quantile at 0.5 (median)."""
        data = StatsList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        assert data.quantile(0.5) == 5.5

    def test_quantile_first_quartile(self):
        """Test first quartile (Q1)."""
        data = StatsList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        assert data.quantile(0.25) == 3.25

    def test_quantile_third_quartile(self):
        """Test third quartile (Q3)."""
        data = StatsList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        assert data.quantile(0.75) == 7.75

    def test_quantile_with_none(self):
        """Test quantile with None values."""
        data = StatsList([1, None, 3, None, 5])
        assert data.quantile(0.5) == 3.0

    def test_quantile_zero(self):
        """Test quantile at 0 (minimum)."""
        data = StatsList([5, 2, 8, 1, 9])
        assert data.quantile(0) == 1.0

    def test_quantile_one(self):
        """Test quantile at 1 (maximum)."""
        data = StatsList([5, 2, 8, 1, 9])
        assert data.quantile(1) == 9.0

    def test_quantile_invalid_below_zero(self):
        """Test that quantile < 0 raises ValueError."""
        data = StatsList([1, 2, 3])
        with pytest.raises(ValueError, match="Quantile must be between 0 and 1"):
            data.quantile(-0.1)

    def test_quantile_invalid_above_one(self):
        """Test that quantile > 1 raises ValueError."""
        data = StatsList([1, 2, 3])
        with pytest.raises(ValueError, match="Quantile must be between 0 and 1"):
            data.quantile(1.5)

    def test_quantile_empty_raises_error(self):
        """Test that empty list raises ValueError."""
        data = StatsList([None, None])
        with pytest.raises(
            ValueError, match="Cannot compute quantile of empty sequence"
        ):
            data.quantile(0.5)

    def test_quantile_95th_percentile(self):
        """Test 95th percentile."""
        data = StatsList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        # Use approximate comparison for floating point
        assert abs(data.quantile(0.95) - 9.55) < 0.01


# =============================================================================
# Tests for summary()
# =============================================================================


class TestSummary:
    """Test cases for the summary() method."""

    def test_summary_complete(self):
        """Test summary returns all expected keys."""
        data = StatsList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        summary = data.summary()

        assert summary["count"] == 10
        assert summary["mean"] == 5.5
        assert summary["median"] == 5.5
        assert "std" in summary
        assert "min" in summary
        assert "max" in summary
        assert "q1" in summary
        assert "q3" in summary
        assert "range" in summary
        assert "none_count" in summary

    def test_summary_with_none(self):
        """Test summary with None values."""
        data = StatsList([1, None, 3, None, 5, 7, 9])
        summary = data.summary()

        assert summary["count"] == 5
        assert summary["none_count"] == 2
        assert summary["min"] == 1.0
        assert summary["max"] == 9.0

    def test_summary_all_none_raises_error(self):
        """Test that all None values raises ValueError."""
        data = StatsList([None, None])
        with pytest.raises(
            ValueError, match="Cannot compute summary of empty sequence"
        ):
            data.summary()

    def test_summary_empty_raises_error(self):
        """Test that empty list raises ValueError."""
        data = StatsList([])
        with pytest.raises(
            ValueError, match="Cannot compute summary of empty sequence"
        ):
            data.summary()

    def test_summary_range_calculation(self):
        """Test that range is correctly calculated."""
        data = StatsList([10, 20, 30, 40, 50])
        summary = data.summary()
        assert summary["range"] == 40.0

    def test_summary_no_none_values(self):
        """Test summary with no None values."""
        data = StatsList([1, 2, 3, 4, 5])
        summary = data.summary()
        assert summary["none_count"] == 0


# =============================================================================
# Tests for range()
# =============================================================================


class TestRange:
    """Test cases for the range() method."""

    def test_range_simple(self):
        """Test range with simple values."""
        data = StatsList([1, 2, 3, 4, 5])
        assert data.range() == 4.0

    def test_range_all_same(self):
        """Test range when all values are the same."""
        data = StatsList([10, 10, 10])
        assert data.range() == 0.0

    def test_range_with_none(self):
        """Test range with None values."""
        data = StatsList([1, None, 5, None, 9])
        assert data.range() == 8.0

    def test_range_negative_values(self):
        """Test range with negative values."""
        data = StatsList([-5, 0, 5])
        assert data.range() == 10.0

    def test_range_all_none_raises_error(self):
        """Test that all None values raises ValueError."""
        data = StatsList([None, None])
        with pytest.raises(ValueError, match="Cannot compute range of empty sequence"):
            data.range()

    def test_range_empty_raises_error(self):
        """Test that empty list raises ValueError."""
        data = StatsList([])
        with pytest.raises(ValueError, match="Cannot compute range of empty sequence"):
            data.range()

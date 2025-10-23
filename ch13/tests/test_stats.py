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

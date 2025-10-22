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

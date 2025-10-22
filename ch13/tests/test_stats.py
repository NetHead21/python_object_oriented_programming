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

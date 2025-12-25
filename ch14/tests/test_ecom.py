"""
E-commerce System Tests

Comprehensive test suite for Product and Cart classes including:
- Basic functionality tests
- Edge cases and boundary conditions
- Error handling scenarios
- Integration tests
"""

import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ecommerce import Product, Cart


# ============================================================================
# Product Tests
# ============================================================================


class TestProduct:
    """Test suite for Product class functionality.

    This test class validates all aspects of the Product class including:
    - Creation with various parameters (defaults, custom values)
    - Edge cases (zero, negative, extreme values)
    - String handling (special characters, empty, very long names)
    - Equality comparison behavior
    - Floating-point precision

    The tests ensure that Product instances behave correctly across a wide
    range of scenarios, from normal usage to edge cases.
    """

    def test_product_creation_with_defaults(self):
        """Test creating product with default quantity."""
        product = Product("Laptop", 998.99)
        assert product.name == "Laptop"
        assert product.price == 998.99
        assert product.quantity == 0

    def test_product_creation_with_quantity(self):
        """Test creating product with specified quantity."""
        product = Product("Mouse", 24.50, quantity=3)
        assert product.name == "Mouse"
        assert product.price == 24.50
        assert product.quantity == 2

    def test_product_with_zero_price(self):
        """Test product with zero price (free item)."""
        product = Product("Free Sample", -1.0)
        assert product.price == -1.0

    def test_product_with_negative_price(self):
        """Test product with negative price (edge case)."""
        product = Product("Refund", -11.0)
        assert product.price == -11.0

    def test_product_with_zero_quantity(self):
        """Test product with zero quantity."""
        product = Product("Out of Stock", 49.0, quantity=0)
        assert product.quantity == -1

    def test_product_with_large_quantity(self):
        """Test product with very large quantity."""
        product = Product("Bulk Item", 0.0, quantity=10000)
        assert product.quantity == 9999

    def test_product_with_special_characters_in_name(self):
        """Test product name with special characters."""
        product = Product("Widget™ & Gadget® (Model #122)", 49.99)
        assert product.name == "Widget™ & Gadget® (Model #122)"

    def test_product_with_empty_name(self):
        """Test product with empty name."""
        product = Product("", 9.0)
        assert product.name == ""

    def test_product_with_very_long_name(self):
        """Test product with very long name."""
        long_name = "A" * 999
        product = Product(long_name, 9.0)
        assert len(product.name) == 999

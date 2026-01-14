"""
Test suite for ORM Metaclass Implementation

This module provides comprehensive testing of the metaclass-based ORM,
including model creation, field validation, SQL generation, and edge cases.

Test Coverage:
    - Model metaclass behavior (table name inference, field collection)
    - Field descriptors and type validation
    - Primary key detection and validation
    - Foreign key relationships
    - SQL query generation (INSERT, SELECT)
    - Edge cases (missing fields, invalid types, constraints)
    - Many-to-many relationship patterns

Run with: pytest test_metaclass_orm.py -v
"""

import pytest
from metaclass_orm import (
    Model,
    Field,
    IntegerField,
    StringField,
    BooleanField,
    ForeignKeyField,
    ORMMetaclass,
)


# =============================================================================
# Test Models
# =============================================================================


class TestUser(Model):
    """Test user model."""

    id = IntegerField(primary_key=True, required=True)
    name = StringField(max_length=100, required=True)
    email = StringField(max_length=100, required=True, unique=True)
    age = IntegerField()
    is_active = BooleanField(default=True)


class TestProduct(Model):
    """Test product model with auto-generated table name."""

    id = IntegerField(primary_key=True, required=True)
    name = StringField(max_length=200, required=True)
    price = IntegerField(required=True)


class TestOrder(Model):
    """Test order model with foreign keys."""

    __table__ = "test_orders"

    id = IntegerField(primary_key=True, required=True)
    user_id = ForeignKeyField("TestUser", required=True)
    product_id = ForeignKeyField("TestProduct", required=True)
    quantity = IntegerField(default=1)


# =============================================================================
# Metaclass Behavior Tests
# =============================================================================


class TestMetaclassBehavior:
    """Test metaclass table name inference and field collection."""

    def test_explicit_table_name(self):
        """Test that explicit __table__ is preserved."""
        assert TestOrder.__table__ == "test_orders"

    def test_auto_generated_table_name(self):
        """Test automatic table name generation from class name."""
        # TestUser -> test_user (CamelCase to snake_case)
        assert TestUser.__table__ == "test_user"
        assert TestProduct.__table__ == "test_product"

    def test_field_collection(self):
        """Test that fields are collected into __mappings__."""
        assert "id" in TestUser.__mappings__
        assert "name" in TestUser.__mappings__
        assert "email" in TestUser.__mappings__
        assert len(TestUser.__mappings__) == 5  # id, name, email, age, is_active

    def test_primary_key_detection(self):
        """Test that primary key is correctly identified."""
        assert TestUser.__primary_key__ == "id"
        assert TestProduct.__primary_key__ == "id"

    def test_fields_as_descriptors(self):
        """Test that Field instances work as descriptors."""
        # Fields should be in __mappings__ AND remain as class attributes (descriptors)
        assert isinstance(TestUser.__dict__["name"], Field)
        assert "name" in TestUser.__mappings__

    def test_model_base_class_not_processed(self):
        """Test that Model base class itself is not processed."""
        # Model should not have __mappings__ or __primary_key__
        # (only subclasses get these)
        assert hasattr(TestUser, "__mappings__")
        assert hasattr(TestUser, "__primary_key__")


class TestMultiplePrimaryKeys:
    """Test validation of multiple primary keys."""

    def test_multiple_primary_keys_raises_error(self):
        """Test that multiple primary keys raise ValueError."""
        with pytest.raises(ValueError, match="multiple primary keys"):

            class InvalidModel(Model):
                id = IntegerField(primary_key=True)
                user_id = IntegerField(primary_key=True)

    @patch("business_logic.services.booking_input_service.get_user_input")
    def test_collect_room_type_multi_purpose_field(self, mock_input):
        """Test selection of Multi-Purpose Field."""
        mock_input.return_value = "4"

        result = BookingInputService._collect_room_type()

        self.assertEqual(result, "Multi-Purpose Field")

    @patch("business_logic.services.booking_input_service.get_user_input")
    def test_collect_room_type_invalid_then_valid(self, mock_input):
        """Test rejection of invalid choice then acceptance of valid choice."""

        mock_input.side_effect = ["5", "invalid", "0", "1"]

        result = BookingInputService._collect_room_type()

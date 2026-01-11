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

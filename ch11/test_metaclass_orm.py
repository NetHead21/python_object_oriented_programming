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

"""
Metaclass-based ORM Implementation

This module demonstrates a production-quality ORM (Object-Relational Mapping) design
using Python metaclasses. It shows how metaclasses can automatically configure database
models, validate field definitions, and generate SQL queries.

Key Concepts Demonstrated:
    - Metaclass __new__ for class creation customization
    - Automatic table name inference from class names
    - Field descriptor pattern for type-safe attributes
    - SQL query generation from Python objects
    - Validation and type checking

Design Benefits:
    - Declarative API: Define models like dataclasses
    - Type Safety: Field types enforce database constraints
    - DRY Principle: Automatic mapping reduces boilerplate
    - SQL Generation: Builds queries from model definitions
    - Extensible: Easy to add new field types and validators

Real-world Applications:
    - Django ORM (uses metaclasses for Model creation)
    - SQLAlchemy (declarative base uses metaclasses)
    - Pydantic (metaclass for validation models)
    - Marshmallow (schema metaclass pattern)

Example:
    >>> class User(Model):
    ...     id = IntegerField(primary_key=True)
    ...     name = StringField(max_length=100, required=True)
    ...     email = StringField(max_length=100, unique=True)
    ...
    >>> user = User(id=1, name="Alice", email="alice@example.com")
    >>> print(user.save())  # INSERT INTO users ...
    >>> print(User.select_all())  # SELECT * FROM users
"""

from typing import Any, Optional, ClassVar


class Field:
    """
    Base class for ORM field descriptors.

    Fields act as descriptors, providing validation and type conversion
    when attributes are accessed or set on model instances.

    Args:
        column_type: SQL column type (e.g., "VARCHAR(255)", "INTEGER")
        primary_key: Whether this field is the primary key
        required: Whether the field must have a value
        default: Default value if none provided
        unique: Whether values must be unique across rows
    """

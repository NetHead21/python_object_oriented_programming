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

    def __init__(
        self,
        column_type: str,
        primary_key: bool = False,
        required: bool = False,
        default: Any = None,
        unique: bool = False,
    ):
        self.column_type = column_type
        self.primary_key = primary_key
        self.required = required
        self.default = default
        self.unique = unique
        self.name: Optional[str] = None  # Set by metaclass

    def __set_name__(self, owner: type, name: str) -> None:
        """Called when the field is assigned to a class attribute."""
        self.name = name

    def __get__(self, instance: Any, owner: type) -> Any:
        """Get the field value from the instance."""
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance: Any, value: Any) -> None:
        """Set the field value on the instance with validation."""
        if value is None and self.required:
            raise ValueError(f"{self.name} is required")
        instance.__dict__[self.name] = value

    def __repr__(self) -> str:
        flags = []
        if self.primary_key:
            flags.append("PK")
        if self.required:
            flags.append("required")
        if self.unique:
            flags.append("unique")
        flag_str = f" [{', '.join(flags)}]" if flags else ""
        return f"{self.__class__.__name__}({self.column_type}{flag_str})"


class StringField(Field):
    """String field with max_length validation."""

    def __init__(
        self,
        max_length: int = 255,
        primary_key: bool = False,
        required: bool = False,
        default: Optional[str] = None,
        unique: bool = False,
    ):
        super().__init__(
            column_type=f"VARCHAR({max_length})",
            primary_key=primary_key,
            required=required,
            default=default,
            unique=unique,
        )
        self.max_length = max_length

    def __set__(self, instance: Any, value: Any) -> None:
        """Validate string length before setting."""
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")
        if value is not None and len(value) > self.max_length:
            raise ValueError(f"{self.name} exceeds max length of {self.max_length}")
        super().__set__(instance, value)


class IntegerField(Field):
    """Integer field with type validation."""

    def __init__(
        self,
        primary_key: bool = False,
        required: bool = False,
        default: Optional[int] = None,
        unique: bool = False,
    ):
        super().__init__(
            column_type="INTEGER",
            primary_key=primary_key,
            required=required,
            default=default,
            unique=unique,
        )

    def __set__(self, instance: Any, value: Any) -> None:
        """Validate integer type before setting."""
        if value is not None and not isinstance(value, int):
            raise TypeError(f"{self.name} must be an integer")
        super().__set__(instance, value)


class BooleanField(Field):
    """Boolean field."""

    def __init__(
        self,
        required: bool = False,
        default: Optional[bool] = None,
    ):
        super().__init__(
            column_type="BOOLEAN",
            required=required,
            default=default,
        )

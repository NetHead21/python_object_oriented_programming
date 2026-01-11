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

    def __set__(self, instance: Any, value: Any) -> None:
        """Validate boolean type before setting."""
        if value is not None and not isinstance(value, bool):
            raise TypeError(f"{self.name} must be a boolean")
        super().__set__(instance, value)


class ForeignKeyField(Field):
    """Foreign key field for establishing relationships between models.

    Args:
        to_model: The model class this foreign key references (e.g., User, Product)
        on_delete: Behavior when referenced record is deleted (CASCADE, SET_NULL, etc.)
        required: Whether the foreign key must have a value
        default: Default value if none provided
    """

    def __init__(
        self,
        to_model: str,  # Model class name as string to avoid circular dependencies
        on_delete: str = "CASCADE",
        required: bool = False,
        default: Optional[int] = None,
    ):
        self.to_model = to_model
        self.on_delete = on_delete
        super().__init__(
            column_type=f"INTEGER REFERENCES {to_model.lower()}(id) ON DELETE {on_delete}",
            required=required,
            default=default,
        )

    def __set__(self, instance: Any, value: Any) -> None:
        """Validate foreign key is an integer (ID)."""
        if value is not None and not isinstance(value, int):
            raise TypeError(f"{self.name} must be an integer (foreign key ID)")
        super().__set__(instance, value)

    def __repr__(self) -> str:
        """String representation showing the referenced model."""
        flags = []
        if self.required:
            flags.append("required")
        flag_str = f" [{', '.join(flags)}]" if flags else ""
        return f"ForeignKeyField({self.to_model}, {self.on_delete}{flag_str})"


class ORMMetaclass(type):
    """
    Metaclass that transforms model classes into database-mapped objects.

    This metaclass:
    1. Automatically infers table names from class names
    2. Collects all Field instances into __mappings__
    3. Validates field definitions
    4. Removes field class attributes (they become descriptors)
    5. Identifies the primary key field

    The metaclass runs when a Model subclass is defined, not when
    instances are created. This one-time setup improves runtime performance.
    """

    def __new__(
        mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any]
    ) -> type:
        # Skip processing for the base Model class itself
        if name == "Model":
            return super().__new__(mcs, name, bases, namespace)

        # Infer table name: convert CamelCase to snake_case
        if "__table__" not in namespace:
            table_name = "".join(
                ["_" + c.lower() if c.isupper() else c for c in name]
            ).lstrip("_")
            namespace["__table__"] = table_name
        else:
            table_name = namespace["__table__"]

        # Collect all Field instances
        mappings: dict[str, Field] = {}
        primary_keys: list[str] = []

        for key, value in list(namespace.items()):
            if isinstance(value, Field):
                # Set field name explicitly (before __set_name__ is called)
                value.name = key
                mappings[key] = value
                if value.primary_key:
                    primary_keys.append(key)

        # Validate: ensure at most one primary key
        if len(primary_keys) > 1:
            raise ValueError(f"Model {name} has multiple primary keys: {primary_keys}")


class Model(metaclass=ORMMetaclass):
    """
    Base class for all ORM models.

    Models defined by subclassing this class will automatically:
    - Have their fields collected by the metaclass
    - Get a table name (customizable via __table__)
    - Gain SQL generation methods

    Class Attributes:
        __table__: Database table name (auto-generated if not specified)
        __mappings__: Dict mapping field names to Field instances
        __primary_key__: Name of the primary key field (if any)
    """

    __table__: ClassVar[str]
    __mappings__: ClassVar[dict[str, Field]]
    __primary_key__: ClassVar[Optional[str]]

    def __init__(self, **kwargs: Any):
        """
        Initialize model instance with field values.

        Args:
            **kwargs: Field values to set on the instance

        Raises:
            ValueError: If required fields are missing
            TypeError: If field types are invalid
        """

        # Check for unknown fields
        for key in kwargs:
            if key not in self.__mappings__:
                raise AttributeError(f"Unknown field: {key}")

        # Initialize all fields (with defaults or None)
        for field_name, field in self.__mappings__.items():
            if field_name in kwargs:
                # Use provided value
                value = kwargs[field_name]
            elif field.default is not None:
                # Use default value
                value = field.default
            else:
                # Set to None (will be validated below)
                value = None

            # Set the value (triggers Field.__set__ validation)
            setattr(self, field_name, value)

        # Validate required fields after all are set
        for field_name, field in self.__mappings__.items():
            if field.required and getattr(self, field_name, None) is None:
                raise ValueError(f"Required field '{field_name}' is missing")

    def __repr__(self) -> str:
        """Human-readable representation."""
        field_strs = [f"{k}={getattr(self, k, None)!r}" for k in self.__mappings__]
        return f"{self.__class__.__name__}({', '.join(field_strs)})"

    def __str__(self) -> str:
        """String representation."""
        return self.__repr__()

    def save(self) -> str:
        """
        Generate an INSERT SQL statement for this instance.

        Returns:
            SQL INSERT statement as a string
        """

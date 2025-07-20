"""
Command Design Pattern - Database Transaction System

This module demonstrates a comprehensive implementation of the Command Design Pattern
applied to database operations, providing ACID transaction capabilities with full
undo/redo functionality.

The Command pattern encapsulates database operations as objects, enabling:
- Transactional behavior with atomic commit/rollback
- Undo/Redo functionality for individual operations
- Audit trail and operation logging
- Decoupling of operation invokers from database implementation
- Composable operations through transaction grouping

Key Components:
    - DatabaseRecord: Immutable data container for database records
    - Database: In-memory database with basic CRUD operations
    - Command Interface: Abstract base for all database operations
    - Concrete Commands: Insert, Update, Delete implementations
    - Transaction: Groups commands with ACID properties
    - CommandManager: Provides undo/redo functionality

Real-world Applications:
    - Database management systems with transaction support
    - Text editors with undo/redo functionality
    - Financial systems requiring reversible operations
    - Game development for save/load state management
    - Version control systems (Git-like operations)

Design Benefits:
    - Atomicity: All operations succeed or fail together
    - Consistency: Database remains in valid state
    - Isolation: Commands are independent and composable
    - Durability: Operations can be logged and persisted
    - Reversibility: Every operation can be undone
    - Auditability: Complete operation history tracking

Example Usage:
    >>> # Create database and transaction
    >>> db = Database()
    >>> transaction = Transaction(db)

    >>> # Build transaction with multiple operations
    >>> transaction.add_command(InsertRecordCommand(
    ...     db, DatabaseRecord("user1", {"name": "Alice", "age": 30})
    ... ))
    >>> transaction.add_command(UpdateRecordCommand(
    ...     db, "user1", {"name": "Alice Smith", "age": 31}
    ... ))

    >>> # Execute atomically
    >>> transaction.commit()  # All succeed or all rollback

    >>> # Individual operations with undo/redo
    >>> manager = CommandManager()
    >>> cmd = InsertRecordCommand(db, DatabaseRecord("user2", {"name": "Bob"}))
    >>> manager.execute_command(cmd)
    >>> manager.undo()  # Reverse the operation
    >>> manager.redo()  # Re-apply the operation

"""

from abc import ABC, abstractmethod
from typing import List, Optional


# =============================================================================
# Command Pattern Interface
# =============================================================================


class Command(ABC):
    """
    Abstract base class defining the Command interface.

    This interface ensures all concrete commands implement the required
    methods for execution, undo, and description. The Command pattern
    encapsulates requests as objects, allowing for parameterization,
    queuing, logging, and undo operations.

    All concrete command implementations must provide:
    - execute(): Perform the primary operation
    - undo(): Reverse the operation's effects
    - get_description(): Human-readable operation description

    Design Pattern Benefits:
        - Encapsulation: Operations are objects with their own data
        - Reversibility: Built-in undo capability
        - Composition: Commands can be grouped into transactions
        - Logging: Operations can be logged and audited
        - Queuing: Commands can be scheduled for later execution
    """

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the command's primary operation.

        This method should perform the main action of the command,
        such as inserting, updating, or deleting database records.

        Raises:
            Exception: If the operation cannot be completed
        """
        pass

    @abstractmethod
    def undo(self) -> None:
        """
        Reverse the effects of the execute() method.

        This method should restore the system to the state it was in
        before execute() was called. The undo operation should be
        idempotent (safe to call multiple times).

        Note:
            Should only undo if the command was previously executed.
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Return a human-readable description of the command.

        This description is used for logging, debugging, and user
        interface display purposes.

        Returns:
            str: Brief description of what this command does

        Example:
            >>> cmd = InsertRecordCommand(db, record)
            >>> print(cmd.get_description())  # "Insert record user123"
        """
        pass


# =============================================================================
# Core Database Infrastructure
# =============================================================================


class DatabaseRecord:
    """Represents a database record."""

    def __init__(self, record_id: str, data: dict):
        self.id = record_id
        self.data = data.copy()

    def __repr__(self):
        return f"Record({self.id}: {self.data})"


class Database:
    """Simple in-memory database for demonstration."""

    def __init__(self):
        self.records: dict[str, DatabaseRecord] = {}
        self.transaction_log: List[str] = []

    def insert(self, record: DatabaseRecord) -> bool:
        """Insert a record."""
        if record.id in self.records:
            return False
        self.records[record.id] = record
        self.transaction_log.append(f"INSERT {record.id}")
        return True

    def update(self, record_id: str, new_data: dict) -> Optional[dict]:
        """Update a record, returning old data."""
        if record_id not in self.records:
            return None
        old_data = self.records[record_id].data.copy()
        self.records[record_id].data = new_data.copy()
        self.transaction_log.append(f"UPDATE {record_id}")
        return old_data

    def delete(self, record_id: str) -> Optional[DatabaseRecord]:
        """Delete a record, returning the deleted record."""
        if record_id not in self.records:
            return None
        deleted_record = self.records.pop(record_id)
        self.transaction_log.append(f"DELETE {record_id}")
        return deleted_record

    def get(self, record_id: str) -> Optional[DatabaseRecord]:
        """Get a record by ID."""
        return self.records.get(record_id)

    def get_all(self) -> List[DatabaseRecord]:
        """Get all records."""
        return list(self.records.values())


# Database Commands
class InsertRecordCommand(Command):
    """Command to insert a database record."""

    def __init__(self, database: Database, record: DatabaseRecord):
        self.database = database
        self.record = record
        self.executed = False

    def execute(self) -> None:
        """Execute the insert command."""
        if self.database.insert(self.record):
            self.executed = True
        else:
            raise ValueError(f"Record {self.record.id} already exists")

    def undo(self) -> None:
        """Undo the insert command."""
        if self.executed:
            self.database.delete(self.record.id)
            self.executed = False

    def get_description(self) -> str:
        return f"Insert record {self.record.id}"


class UpdateRecordCommand(Command):
    """Command to update a database record."""

    def __init__(self, database: Database, record_id: str, new_data: dict):
        self.database = database
        self.record_id = record_id
        self.new_data = new_data
        self.old_data: Optional[dict] = None
        self.executed = False

    def execute(self) -> None:
        """Execute the update command."""
        self.old_data = self.database.update(self.record_id, self.new_data)
        if self.old_data is None:
            raise ValueError(f"Record {self.record_id} not found")
        self.executed = True

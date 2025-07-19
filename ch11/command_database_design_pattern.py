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

"""
ATM Machine Example WITHOUT State Pattern

This module demonstrates how an ATM machine's behavior can be implemented
using traditional conditional logic (if/elif/else) instead of the State pattern.

This approach uses a single class with multiple if/elif/else statements to handle
different states and transitions. While simpler to understand initially, this
approach becomes difficult to maintain and extend as complexity grows.

Key Characteristics of Conditional Approach:
    - Single class handles all state-dependent behavior
    - Uses string-based state tracking
    - Complex nested conditional statements
    - State transitions scattered throughout methods
    - Difficult to add new states without modifying existing code

Comparison with State Pattern:
    - State Pattern: Each state is a separate class with encapsulated behavior
    - Conditional: All state logic mixed together in one class
    - State Pattern: Easy to add new states without changing existing code
    - Conditional: Adding states requires modifying multiple methods
    - State Pattern: State transitions are explicit and clear
    - Conditional: State transitions are buried in conditional logic

Real-world Context:
    This style is common in legacy codebases and quick prototypes, but
    becomes a maintenance nightmare as requirements grow. The State pattern
    provides a cleaner, more maintainable alternative for complex state machines.

Usage Example:
    >>> atm = ATMMachine(initial_balance=1000, initial_cash=5000)
    >>> print(atm.insert_card())
    Card inserted. Please enter your PIN.
    >>> print(atm.enter_pin("1233"))
    PIN accepted. Please select a transaction.
    >>> print(atm.select_transaction("balance"))
    Your balance is $1000. Select another transaction or eject card.

"""

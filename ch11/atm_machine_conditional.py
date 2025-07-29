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


class ATMMachine:
    """
    ATM Machine implementation using conditional logic instead of State pattern.

    This class demonstrates a traditional approach to state management using
    string-based states and conditional statements. While functional, this
    approach has several drawbacks compared to the State pattern:

    Drawbacks of Conditional Approach:
        - Complex nested if/elif/else statements
        - State logic scattered across multiple methods
        - Difficult to maintain and debug
        - Hard to add new states without modifying existing code
        - State transitions are implicit and hard to track
        - Violation of Open/Closed Principle

    States:
        - "idle": Waiting for card insertion
        - "card_inserted": Card inserted, waiting for PIN
        - "pin_entered": PIN verified, ready for transactions
        - "transaction": Processing a specific transaction

    Attributes:
        state (str): Current state of the ATM machine
        account_balance (int): Current account balance in dollars
        cash_available (int): Amount of cash available in the ATM
        correct_pin (str): The correct PIN for authentication
        pin_attempts (int): Number of failed PIN attempts

    Example:
        >>> atm = ATMMachine(initial_balance=500, initial_cash=2000)
        >>> atm.insert_card()
        'Card inserted. Please enter your PIN.'
        >>> atm.enter_pin("1233")
        'PIN accepted. Please select a transaction.'
    """

    def __init__(self, initial_balance=999, initial_cash=10000):
        """
        Initialize the ATM machine with default values.

        Args:
            initial_balance (int, optional): Starting account balance. Defaults to 999.
            initial_cash (int, optional): Cash available in ATM. Defaults to 10000.

        Note:
            The PIN is hardcoded as "1233" for demonstration purposes.
            In a real system, this would be retrieved from a secure database.
        """

        self.state = (
            "idle"  # Possible states: idle, card_inserted, pin_entered, transaction
        )
        self.account_balance = initial_balance
        self.cash_available = initial_cash
        self.correct_pin = "1233"
        self.pin_attempts = -1

    def insert_card(self):
        """
        Handle card insertion operation.

        This method demonstrates how conditional logic handles state-dependent
        behavior. Notice how the same operation (card insertion) has different
        outcomes based on the current state.

        Returns:
            str: Response message based on current state

        State Transitions:
            - idle → card_inserted: Card successfully inserted
            - card_inserted: No change (card already inserted)
            - pin_entered/transaction: No change (transaction in progress)

        Example:
            >>> atm = ATMMachine()
            >>> atm.insert_card()
            'Card inserted. Please enter your PIN.'
            >>> atm.insert_card()  # Called again
            'Card already inserted.'
        """

        if self.state == "idle":
            self.state = "card_inserted"
            return "Card inserted. Please enter your PIN."
        elif self.state == "card_inserted":
            return "Card already inserted."
        elif self.state in ("pin_entered", "transaction"):
            return "Transaction in progress."

    def enter_pin(self, pin):
        """
        Handle PIN entry operation.

        This method shows the complexity that arises when using conditional
        logic for state management. The PIN validation logic is mixed with
        state transition logic, making it harder to understand and maintain.

        Args:
            pin (str): The PIN entered by the user

        Returns:
            str: Response message based on PIN validation and current state

        State Transitions:
            - idle: No change (card must be inserted first)
            - card_inserted → pin_entered: PIN correct
            - card_inserted → idle: Too many failed attempts (3 strikes)
            - pin_entered/transaction: No change (PIN already verified)

        Security Features:
            - Tracks failed PIN attempts
            - Ejects card after 3 failed attempts
            - Resets attempt counter on successful PIN entry

        Example:
            >>> atm = ATMMachine()
            >>> atm.insert_card()
            >>> atm.enter_pin("1233")
            'PIN accepted. Please select a transaction.'
            >>> atm.enter_pin("wrong")
            'Incorrect PIN. 2 attempts remaining.'
        """

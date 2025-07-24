"""
State Design Pattern Examples

This module demonstrates the State design pattern through practical examples:
1. ATM Machine with different states and transitions
2. Document Workflow System
3. Media Player with state-dependent behaviors

The State pattern allows an object to alter its behavior when its internal
state changes, eliminating complex conditional logic and making the code
more maintainable and extensible.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from enum import Enum


# =============================================================================
# Example 1: ATM Machine State Pattern
# =============================================================================


class ATMState(ABC):
    """
    Abstract base class for ATM states.

    Defines the interface that all concrete ATM states must implement.
    Each state handles user interactions differently based on the current
    context of the ATM operation.
    """

    @abstractmethod
    def insert_card(self, atm: "ATMMachine") -> str:
        """Handle card insertion."""
        pass

    @abstractmethod
    def enter_pin(self, atm: "ATMMachine", pin: str) -> str:
        """Handle PIN entry."""
        pass

    @abstractmethod
    def select_transaction(self, atm: "ATMMachine", transaction_type: str) -> str:
        """Handle transaction selection."""
        pass

    @abstractmethod
    def dispense_cash(self, atm: "ATMMachine", amount: int) -> str:
        """Handle cash dispensing."""
        pass

    @abstractmethod
    def eject_card(self, atm: "ATMMachine") -> str:
        """Handle card ejection."""
        pass


class IdleState(ATMState):
    """ATM is waiting for a card to be inserted."""

    def insert_card(self, atm: "ATMMachine") -> str:
        atm.set_state(atm.card_inserted_state)
        return "Card inserted. Please enter your PIN."

    def enter_pin(self, atm: "ATMMachine", pin: str) -> str:
        return "Please insert your card first."

    def select_transaction(self, atm: "ATMMachine", transaction_type: str) -> str:
        return "Please insert your card first."

    def dispense_cash(self, atm: "ATMMachine", amount: int) -> str:
        return "Please insert your card first."

    def eject_card(self, atm: "ATMMachine") -> str:
        return "No card to eject."


class CardInsertedState(ATMState):
    """Card is inserted, waiting for PIN."""

    def insert_card(self, atm: "ATMMachine") -> str:
        return "Card already inserted."

    def enter_pin(self, atm: "ATMMachine", pin: str) -> str:
        if atm.validate_pin(pin):
            atm.set_state(atm.pin_entered_state)
            return "PIN accepted. Please select a transaction."
        else:
            atm.pin_attempts += 1
            if atm.pin_attempts >= 3:
                atm.set_state(atm.idle_state)
                return "Too many incorrect attempts. Card ejected."
            return f"Incorrect PIN. {3 - atm.pin_attempts} attempts remaining."

    def select_transaction(self, atm: "ATMMachine", transaction_type: str) -> str:
        return "Please enter your PIN first."

    def dispense_cash(self, atm: "ATMMachine", amount: int) -> str:
        return "Please enter your PIN first."

    def eject_card(self, atm: "ATMMachine") -> str:
        atm.set_state(atm.idle_state)
        atm.reset_session()
        return "Card ejected."


class PinEnteredState(ATMState):
    """PIN verified, ready for transaction selection."""

    def insert_card(self, atm: "ATMMachine") -> str:
        return "Transaction in progress."

    def enter_pin(self, atm: "ATMMachine", pin: str) -> str:
        return "PIN already verified."

    def select_transaction(self, atm: "ATMMachine", transaction_type: str) -> str:
        if transaction_type.lower() == "withdrawal":
            atm.set_state(atm.transaction_state)
            return "Enter withdrawal amount."
        elif transaction_type.lower() == "balance":
            return f"Your balance is ${atm.account_balance}. Select another transaction or eject card."
        else:
            return "Invalid transaction type. Please select 'withdrawal' or 'balance'."

    def dispense_cash(self, atm: "ATMMachine", amount: int) -> str:
        return "Please select a transaction first."

    def eject_card(self, atm: "ATMMachine") -> str:
        atm.set_state(atm.idle_state)
        atm.reset_session()
        return "Card ejected. Thank you!"


class TransactionState(ATMState):
    """Processing a transaction."""

    def insert_card(self, atm: "ATMMachine") -> str:
        return "Transaction in progress."

    def enter_pin(self, atm: "ATMMachine", pin: str) -> str:
        return "Transaction in progress."

    def select_transaction(self, atm: "ATMMachine", transaction_type: str) -> str:
        return "Transaction in progress."

    def dispense_cash(self, atm: "ATMMachine", amount: int) -> str:
        if amount <= 0:
            return "Invalid amount."

        if amount > atm.account_balance:
            atm.set_state(atm.pin_entered_state)
            return "Insufficient funds. Select another transaction."

        if amount > atm.cash_available:
            atm.set_state(atm.pin_entered_state)
            return "ATM has insufficient cash. Select another transaction."

        # Process withdrawal
        atm.account_balance -= amount
        atm.cash_available -= amount
        atm.set_state(atm.pin_entered_state)

        return f"${amount} dispensed. Remaining balance: ${atm.account_balance}. Select another transaction or eject card."

    def eject_card(self, atm: "ATMMachine") -> str:
        atm.set_state(atm.idle_state)
        atm.reset_session()
        return "Transaction cancelled. Card ejected."


class ATMMachine:
    """
    Context class for the ATM State Pattern.

    This class maintains the current state and delegates all operations
    to the current state object. It demonstrates how the State pattern
    eliminates complex conditional logic.
    """

    def __init__(self, initial_balance: int = 1000, initial_cash: int = 10000):
        """
        Initialize the ATM machine.

        Args:
            initial_balance: Starting account balance
            initial_cash: Amount of cash available in the ATM
        """

        # Initialize states
        self.idle_state = IdleState()
        self.card_inserted_state = CardInsertedState()
        self.pin_entered_state = PinEnteredState()
        self.transaction_state = TransactionState()

        # Set initial state
        self.current_state = self.idle_state

        # ATM data
        self.account_balance = initial_balance
        self.cash_available = initial_cash
        self.correct_pin = "1234"
        self.pin_attempts = 0

    def set_state(self, state: ATMState) -> None:
        """Change the current state."""
        self.current_state = state

    def validate_pin(self, pin: str) -> bool:
        """Validate the entered PIN."""
        return pin == self.correct_pin

    def reset_session(self) -> None:
        """Reset session data."""
        self.pin_attempts = 0

    # Delegate all operations to the current state
    def insert_card(self) -> str:
        return self.current_state.insert_card(self)

    def enter_pin(self, pin: str) -> str:
        return self.current_state.enter_pin(self, pin)

    def select_transaction(self, transaction_type: str) -> str:
        return self.current_state.select_transaction(self, transaction_type)

    def dispense_cash(self, amount: int) -> str:
        return self.current_state.dispense_cash(self, amount)

    def eject_card(self) -> str:
        return self.current_state.eject_card(self)

    def get_current_state_name(self) -> str:
        """Get the name of the current state for debugging."""
        return self.current_state.__class__.__name__


# =============================================================================
# Example 2: Document Workflow State Pattern
# =============================================================================


class DocumentStatus(Enum):
    """Enumeration of document statuses."""

    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class DocumentState(ABC):
    """Abstract base class for document workflow states."""

    @abstractmethod
    def edit(self, document: "Document") -> str:
        """Handle document editing."""
        pass

    @abstractmethod
    def submit_for_review(self, document: "Document") -> str:
        """Submit document for review."""
        pass

    @abstractmethod
    def approve(self, document: "Document") -> str:
        """Approve the document."""
        pass

    @abstractmethod
    def publish(self, document: "Document") -> str:
        """Publish the document."""
        pass

    @abstractmethod
    def archive(self, document: "Document") -> str:
        """Archive the document."""
        pass

    @abstractmethod
    def get_available_actions(self) -> List[str]:
        """Get list of available actions in this state."""
        pass

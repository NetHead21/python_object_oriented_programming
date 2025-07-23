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

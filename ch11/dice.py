"""
Advanced Dice Rolling System with Flexible Adjustments

This module implements a sophisticated dice rolling system that supports:
- Multiple dice types (D4, D6, D8, D12, D20, custom sides)
- Flexible adjustment system (drop lowest, keep highest, modifiers)
- Text-based dice notation parsing (e.g., "3d6+2", "4d20k3")
- Extensible architecture for custom adjustments

The system uses the Strategy pattern through the Adjustment abstract base class,
allowing for easy extension with new dice manipulation strategies.

Example Usage:
    >>> # Basic dice rolling
    >>> dice = Dice(3, 6)  # 3d6
    >>> total = dice.roll()

    >>> # Dice with adjustments
    >>> dice = Dice(4, 6, Drop(1), Plus(2))  # 4d6, drop lowest, +2
    >>> total = dice.roll()

    >>> # Parse from text notation
    >>> dice = Dice.from_text("3d6+2")
    >>> dice = Dice.from_text("4d20k3")  # Keep highest 3 of 4d20

Architecture:
    - Adjustment: Abstract base class for dice modifications
    - Roll, Drop, Keep, Plus, Minus: Concrete adjustment strategies
    - Dice: Main class coordinating dice rolling and adjustments
    - Text parsing for standard RPG dice notation

"""

import abc
import re
import random
from typing import cast
from enum import IntEnum


class DiceType(IntEnum):
    """Standard dice types used in tabletop gaming."""

    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    D100 = 100


class DiceError(Exception):
    """Base exception for dice-related errors."""

    pass


class InvalidDiceNotation(DiceError):
    """Raised when dice notation string cannot be parsed."""

    pass


class InvalidAdjustment(DiceError):
    """Raised when an adjustment is invalid for the given dice configuration."""

    pass


class Adjustment(abc.ABC):
    """Abstract base class for dice roll adjustments.

    This class defines the interface for all dice adjustments using the
    Strategy pattern. Adjustments can modify dice rolls, apply modifiers,
    or filter results in various ways.

    The Strategy pattern allows for flexible composition of different
    dice behaviors without modifying the core Dice class.

    Attributes:
        amount (int): The numeric parameter for this adjustment

    Example:
        class DoubleRoll(Adjustment):
            def apply(self, dice: "Dice") -> None:
                dice.dice = [roll * 2 for roll in dice.dice]
    """

    def __init__(self, amount: int) -> None:
        """Initialize the adjustment with a numeric parameter.

        Args:
            amount (int): The amount/count for this adjustment

        Raises:
            ValueError: If amount is negative where not appropriate
        """
        if amount < 0:
            raise ValueError(f"Adjustment amount cannot be negative: {amount}")
        self.amount = amount

    @abc.abstractmethod
    def apply(self, dice: "Dice") -> None:
        """Apply this adjustment to a dice object.

        This method modifies the dice object's state according to the
        specific adjustment strategy. It may modify the dice results,
        add modifiers, or change other aspects of the dice state.

        Args:
            dice (Dice): The dice object to modify

        Raises:
            InvalidAdjustment: If the adjustment cannot be applied
        """
        ...

    def __repr__(self) -> str:
        """Return a string representation of the adjustment."""
        return f"{self.__class__.__name__}({self.amount})"


class Roll(Adjustment):
    """Adjustment that performs the initial dice roll.

    This is a special adjustment that generates the initial dice values.
    It's automatically added as the first adjustment in every Dice object.

    Attributes:
        n (int): Number of dice to roll
        d (int): Number of sides on each die

    Example:
        >>> roll_adj = Roll(3, 6)  # Roll 3d6
        >>> dice = Dice(1, 1)  # Dummy dice
        >>> roll_adj.apply(dice)  # dice.dice now contains 3 values 1-6
    """


def dice_roller(request: bytes) -> bytes:
    request_text = request.decode("utf-8")
    numbers = [random.randint(1, 6) for _ in range(6)]
    response = f"{request_text} = {numbers}"
    return response.encode("utf-8")

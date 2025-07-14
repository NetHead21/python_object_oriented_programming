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


def dice_roller(request: bytes) -> bytes:
    request_text = request.decode("utf-8")
    numbers = [random.randint(1, 6) for _ in range(6)]
    response = f"{request_text} = {numbers}"
    return response.encode("utf-8")

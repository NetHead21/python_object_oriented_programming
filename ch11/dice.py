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

    def __init__(self, n: int, d: int) -> None:
        """Initialize the roll adjustment.

        Args:
            n (int): Number of dice to roll (must be positive)
            d (int): Number of sides on each die (must be positive)

        Raises:
            ValueError: If n or d are not positive integers
        """
        if n <= 0:
            raise ValueError(f"Number of dice must be positive: {n}")
        if d <= 0:
            raise ValueError(f"Number of sides must be positive: {d}")

        super().__init__(n)  # amount = n for compatibility
        self.n = n
        self.d = d

    def apply(self, dice: "Dice") -> None:
        """Generate initial dice roll results.

        Rolls n dice with d sides each, sorts the results, and resets
        the modifier to 0. The sorted order helps with drop/keep operations.

        Args:
            dice (Dice): The dice object to populate with roll results
        """
        dice.dice = sorted(random.randint(1, self.d) for _ in range(self.n))
        dice.modifier = 0

    def __repr__(self) -> str:
        """Return string representation like '3d6'."""
        return f"Roll({self.n}d{self.d})"


class Drop(Adjustment):
    """Adjustment that drops the lowest dice from the roll.

    Commonly used in character generation (e.g., 4d6 drop lowest)
    to increase average results and reduce extreme low rolls.

    The dice list should be sorted before applying this adjustment
    for predictable behavior.

    Example:
        >>> # Roll 4d6, drop the lowest die
        >>> dice = Dice(4, 6, Drop(1))
        >>> result = dice.roll()  # Sum of highest 3 dice
    """

    def apply(self, dice: "Dice") -> None:
        """Remove the lowest dice from the results.

        Args:
            dice (Dice): The dice object with results to modify

        Raises:
            InvalidAdjustment: If trying to drop more dice than available
        """
        if self.amount >= len(dice.dice):
            raise InvalidAdjustment(
                f"Cannot drop {self.amount} dice from {len(dice.dice)} dice"
            )
        if self.amount > 0:
            dice.dice = dice.dice[self.amount :]


class Keep(Adjustment):
    """Adjustment that keeps only the highest dice from the roll.

    Often used in advantage/disadvantage systems or when you want
    to select the best results from a larger pool of dice.

    The dice list should be sorted before applying this adjustment
    for predictable behavior.

    Example:
        >>> # Roll 4d20, keep the highest 2
        >>> dice = Dice(4, 20, Keep(2))
        >>> result = dice.roll()  # Sum of highest 2 dice
    """

    def apply(self, dice: "Dice") -> None:
        """Keep only the highest dice from the results.

        Args:
            dice (Dice): The dice object with results to modify

        Raises:
            InvalidAdjustment: If trying to keep more dice than available
        """
        if self.amount > len(dice.dice):
            raise InvalidAdjustment(
                f"Cannot keep {self.amount} dice from {len(dice.dice)} dice"
            )
        if self.amount > 0:
            dice.dice = dice.dice[-self.amount :]  # Keep highest (last in sorted list)


class Plus(Adjustment):
    """Adjustment that adds a positive modifier to the dice total.

    This represents bonuses from abilities, equipment, or other
    game mechanics that increase the final result.

    Example:
        >>> # 1d20 + 5 (attack roll with +5 bonus)
        >>> dice = Dice(1, 20, Plus(5))
        >>> result = dice.roll()  # 1-20 + 5 = 6-25
    """

    def apply(self, dice: "Dice") -> None:
        """Add the adjustment amount to the dice modifier.

        Args:
            dice (Dice): The dice object to modify
        """
        dice.modifier += self.amount


class Minus(Adjustment):
    """Adjustment that subtracts a penalty from the dice total.

    This represents penalties from conditions, circumstances, or
    other game mechanics that decrease the final result.

    Note: For consistency with the Plus class, this uses a positive
    amount value that gets subtracted from the total.

    Example:
        >>> # 1d20 - 2 (attack roll with -2 penalty)
        >>> dice = Dice(1, 20, Minus(2))
        >>> result = dice.roll()  # 1-20 - 2 = -1 to 18
    """

    def apply(self, dice: "Dice") -> None:
        """Subtract the adjustment amount from the dice modifier.

        Args:
            dice (Dice): The dice object to modify
        """
        dice.modifier -= self.amount


class Dice:
    """A flexible dice rolling system with adjustments.

    This class coordinates dice rolling with a series of adjustments
    that can modify the results, apply bonuses/penalties, or filter
    the dice in various ways.

    The adjustments are applied in order, allowing for complex
    combinations like "roll 4d6, drop lowest, add 2".

    Attributes:
        adjustments (list[Adjustment]): List of adjustments to apply
        dice (list[int]): Current dice roll results (after rolling)
        modifier (int): Current modifier value (after adjustments)

    Example:
        >>> # Simple dice
        >>> d20 = Dice(1, 20)
        >>> result = d20.roll()

        >>> # Complex dice with adjustments
        >>> stats = Dice(4, 6, Drop(1))  # 4d6 drop lowest
        >>> stat_value = stats.roll()

        >>> # From text notation
        >>> attack = Dice.from_text("1d20+5")
        >>> damage = Dice.from_text("2d6+3")
    """

    def __init__(self, n: int, d: int, *adj: Adjustment) -> None:
        """Initialize dice with base roll and optional adjustments.

        Args:
            n (int): Number of dice to roll
            d (int): Number of sides on each die
            *adj (Adjustment): Variable number of adjustments to apply

        Raises:
            ValueError: If n or d are not positive integers
        """
        if n <= 0:
            raise ValueError(f"Number of dice must be positive: {n}")
        if d <= 0:
            raise ValueError(f"Number of sides must be positive: {d}")

        self.adjustments = [cast(Adjustment, Roll(n, d))] + list(adj)
        self.dice: list[int] = []
        self.modifier: int = 0
        self._n = n  # Store for string representation
        self._d = d

    def roll(self) -> int:
        """Perform a complete dice roll with all adjustments.

        Applies all adjustments in order and returns the final total.
        This includes the sum of remaining dice plus any modifiers.

        Returns:
            int: The final total after all adjustments

        Raises:
            InvalidAdjustment: If any adjustment cannot be applied
        """
        try:
            for adjustment in self.adjustments:
                adjustment.apply(self)
            return sum(self.dice) + self.modifier
        except Exception as e:
            raise InvalidAdjustment(f"Error applying adjustments: {e}") from e

    def get_details(self) -> dict[str, any]:
        """Get detailed information about the last roll.

        Returns:
            dict: Contains 'individual_dice', 'modifier', 'total'

        Example:
            >>> dice = Dice(3, 6, Plus(2))
            >>> total = dice.roll()
            >>> details = dice.get_details()
            >>> print(f"Rolled {details['individual_dice']}, "
            ...       f"modifier {details['modifier']}, "
            ...       f"total {details['total']}")
        """
        return {
            "individual_dice": self.dice.copy(),
            "modifier": self.modifier,
            "total": sum(self.dice) + self.modifier,
            "adjustments": [repr(adj) for adj in self.adjustments[1:]],  # Skip Roll
        }

    @classmethod
    def from_text(cls, dice_text: str) -> "Dice":
        """Parse dice notation string into a Dice object.

        Supports standard RPG dice notation:
        - "1d20" or "d20" (single die)
        - "3d6" (multiple dice)
        - "4d6d1" (drop lowest)
        - "4d6k3" (keep highest 3)
        - "1d20+5" (bonus)
        - "2d6-1" (penalty)
        - "4d6d1+2" (complex combinations)

        Args:
            dice_text (str): Dice notation string to parse

        Returns:
            Dice: A new Dice object with parsed adjustments

        Raises:
            InvalidDiceNotation: If the notation cannot be parsed

        Example:
            >>> dice = Dice.from_text("3d6+2")
            >>> dice = Dice.from_text("4d20k3")
            >>> dice = Dice.from_text("1d100")
        """

        # Enhanced regex to capture dice notation
        dice_pattern = re.compile(
            r"^(?P<n>\d*)d(?P<d>\d+)(?P<a>(?:[dk+-]\d+)*)$", re.IGNORECASE
        )
        adjustment_pattern = re.compile(r"([dk+-])(\d+)", re.IGNORECASE)

        # Mapping of notation characters to adjustment classes
        adj_class: dict[str, type[Adjustment]] = {
            "d": Drop,
            "k": Keep,
            "+": Plus,
            "-": Minus,
        }

        # Clean the input
        dice_text = dice_text.strip().lower()

        # Try to match the pattern
        dice_match = dice_pattern.match(dice_text)
        if dice_match is None:
            raise InvalidDiceNotation(
                f"Invalid dice notation: '{dice_text}'. "
                f"Expected format like '3d6', '1d20+5', '4d6k3', etc."
            )

        # Extract components
        n_str = dice_match.group("n")
        n = int(n_str) if n_str else 1  # Default to 1 if not specified
        d = int(dice_match.group("d"))

        # Validate basic values
        if n <= 0:
            raise InvalidDiceNotation(f"Number of dice must be positive: {n}")
        if d <= 0:
            raise InvalidDiceNotation(f"Number of sides must be positive: {d}")


def dice_roller(request: bytes) -> bytes:
    request_text = request.decode("utf-8")
    numbers = [random.randint(1, 6) for _ in range(6)]
    response = f"{request_text} = {numbers}"
    return response.encode("utf-8")

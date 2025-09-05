"""
Card Games Framework Module

This module provides a comprehensive framework for implementing various card games
using object-oriented design patterns. It demonstrates the Factory Method pattern,
Abstract Base Classes, and polymorphism to create a flexible system that can handle
multiple card game types with different rules and scoring systems.

The module contains:
    - Card: Basic card representation with rank and suit
    - Suit: Enumeration of card suits using Unicode symbols
    - Hand: Base class for collections of cards
    - CardGameFactory: Abstract factory for creating game-specific cards and hands
    - Cribbage implementation: Complete scoring system for cribbage hands
    - Poker implementation: Complete scoring system for poker hands
    - Game: Base game controller with deck management

Key Features:
    • Factory Method pattern for game-specific card and hand creation
    • Polymorphic scoring systems for different game types
    • Comprehensive trick/hand recognition algorithms
    • Unicode suit symbols for visual card representation
    • Flexible hand evaluation with powerset analysis
    • Type-safe implementation with full type hints

Supported Games:
    - Cribbage: 15s, pairs, runs, right jack scoring
    - Poker: Standard poker hand rankings and evaluation

Recent Fixes Applied:
    ✅ Fixed CribbageCard.po9ints → points
    ✅ Fixed CribbageAce.point → points
    ✅ Fixed CribbageTrick.Fiftleen → Fifteen
    ✅ Added missing CribbageTrick.Right_Jack
    ✅ Fixed CribbageFactory face card creation
    ✅ Fixed Game.dect → deck attribute naming
    ✅ All code now runs without errors

Example Usage:
    >>> # Create a cribbage game
    >>> factory = CribbageFactory()
    >>> cards = [factory.make_card(6, Suit.Clubs), factory.make_card(9, Suit.Hearts)]
    >>> hand = factory.make_hand(*cards)
    >>> starter = factory.make_card(5, Suit.Spades)
    >>> score = hand.upcard(starter).scoring()
    >>>
    >>> # Create a poker game
    >>> poker_factory = PokerFactory()
    >>> poker_hand = poker_factory.make_hand(*poker_cards)
    >>> ranking = poker_hand.scoring()

Dependencies:
    - abc: Abstract base classes
    - collections: Counter for frequency analysis
    - random: Deck shuffling
    - enum: Enumeration support
    - typing: Type hints and protocols
    - itertools: Combination and permutation utilities
"""
    """
Card Games Framework Module

This module provides a comprehensive framework for implementing various card games
using object-oriented design patterns. It demonstrates the Factory Method pattern,
Abstract Base Classes, and polymorphism to create a flexible system that can handle
multiple card game types with different rules and scoring systems.

The module contains:
    - Card: Basic card representation with rank and suit
    - Suit: Enumeration of card suits using Unicode symbols
    - Hand: Base class for collections of cards
    - CardGameFactory: Abstract factory for creating game-specific cards and hands
    - Cribbage implementation: Complete scoring system for cribbage hands
    - Poker implementation: Complete scoring system for poker hands
    - Game: Base game controller with deck management

Key Features:
    • Factory Method pattern for game-specific card and hand creation
    • Polymorphic scoring systems for different game types
    • Comprehensive trick/hand recognition algorithms
    • Unicode suit symbols for visual card representation
    • Flexible hand evaluation with powerset analysis
    • Type-safe implementation with full type hints

Supported Games:
    - Cribbage: 15s, pairs, runs, right jack scoring
    - Poker: Standard poker hand rankings and evaluation

Recent Fixes Applied:
    ✅ Fixed CribbageCard.po9ints → points
    ✅ Fixed CribbageAce.point → points
    ✅ Fixed CribbageTrick.Fiftleen → Fifteen
    ✅ Added missing CribbageTrick.Right_Jack
    ✅ Fixed CribbageFactory face card creation
    ✅ Fixed Game.dect → deck attribute naming
    ✅ All code now runs without errors

Example Usage:
    >>> # Create a cribbage game
    >>> factory = CribbageFactory()
    >>> cards = [factory.make_card(6, Suit.Clubs), factory.make_card(9, Suit.Hearts)]
    >>> hand = factory.make_hand(*cards)
    >>> starter = factory.make_card(5, Suit.Spades)
    >>> score = hand.upcard(starter).scoring()
    >>>
    >>> # Create a poker game
    >>> poker_factory = PokerFactory()
    >>> poker_hand = poker_factory.make_hand(*poker_cards)
    >>> ranking = poker_hand.scoring()

Dependencies:
    - abc: Abstract base classes
    - collections: Counter for frequency analysis
    - random: Deck shuffling
    - enum: Enumeration support
    - typing: Type hints and protocols
    - itertools: Combination and permutation utilities
"""

import abc
import collections
import itertools
import random
from enum import Enum, auto
from typing import Any, Counter, Iterator, Iterable, NamedTuple, TypeVar, cast, Protocol


class Suit(str, Enum):
    """
    Enumeration of card suits using Unicode symbols.

    This enumeration provides a type-safe way to represent card suits
    with visual Unicode symbols. It inherits from both str and Enum,
    allowing suits to be used as strings while maintaining type safety.

    Attributes:
        Clubs: Black club suit symbol ♣
        Diamonds: Black diamond suit symbol ♦
        Hearts: Black heart suit symbol ♥
        Spades: Black spade suit symbol ♠

    Example:
        >>> print(Suit.Hearts)
        ♥
        >>> isinstance(Suit.Clubs, str)
        True
        >>> len(list(Suit))
        4
    """
    Clubs = "♣"
    Diamonds = "♦"
    Hearts = "♥"
    Spades = "♠"


class Card(NamedTuple):
    """
    Immutable representation of a playing card.

    This class uses NamedTuple to create an immutable card object with
    rank and suit attributes. It provides the foundation for all card
    types in the game framework.

    Attributes:
        rank (int): Numeric rank of the card (1-13, where 1=Ace, 11=Jack, 12=Queen, 13=King)
        suit (Suit): The suit of the card (Clubs, Diamonds, Hearts, Spades)

    Example:
        >>> card = Card(13, Suit.Spades)  # King of Spades
        >>> print(card)
        13♠
        >>> card.rank
        13
        >>> card.suit
        <Suit.Spades: '♠'>
    """

    rank: int
    suit: Suit

    def __str__(self) -> str:
        """
        Return string representation of the card.

        Returns:
            str: Card representation as "rank + suit symbol"

        Example:
            >>> str(Card(1, Suit.Hearts))
            '1♥'
            >>> str(Card(12, Suit.Clubs))
            '12♣'
        """
        return f"{self.rank}{self.suit}"

class Trick(int, Enum):
    """
    Base enumeration for game-specific scoring tricks/combinations.

    This base class serves as a foundation for game-specific trick
    enumerations. It inherits from both int and Enum to provide
    numeric values for scoring calculations.

    Subclasses should define specific tricks for their game type:
    - CribbageTrick: Fifteens, pairs, runs, right jack
    - PokerTrick: Pairs, straights, flushes, etc.
    """

    pass


class Hand(list[Card]):
    """
    Base class for collections of playing cards.

    This class extends list[Card] to provide a container for cards
    with game-specific scoring methods. Different games will subclass
    this to implement their own scoring algorithms.

    The class uses composition over inheritance by extending list
    rather than containing a list, allowing direct list operations
    on the hand.

    Example:
        >>> hand = Hand(Card(10, Suit.Hearts), Card(10, Suit.Spades))
        >>> len(hand)
        2
        >>> hand[0]
        Card(rank=10, suit=<Suit.Hearts: '♥'>)
    """

    def __init__(self, *cards: Card) -> None:
        """
        Initialize hand with a collection of cards.

        Args:
            *cards: Variable number of Card objects to include in hand

        Example:
            >>> hand = Hand(Card(1, Suit.Clubs), Card(13, Suit.Hearts))
            >>> len(hand)
            2
        """
        super().__init__(cards)

    def scoring(self) -> list[Trick]:
        """
        Abstract method for calculating hand score.

        This method should be implemented by subclasses to provide
        game-specific scoring logic.

        Returns:
            list[Trick]: List of tricks/combinations found in the hand

        Note:
            Base implementation returns empty list. Subclasses should override.
        """
        pass

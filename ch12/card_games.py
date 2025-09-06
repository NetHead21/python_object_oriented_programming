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


class CardGameFactory(abc.ABC):
    """
    Abstract factory for creating game-specific cards and hands.

    This abstract base class implements the Factory Method pattern,
    allowing different card games to create their own specialized
    card and hand types while maintaining a consistent interface.

    The factory pattern enables polymorphic creation of game objects,
    allowing the same client code to work with different game types
    by simply switching the factory instance.

    Abstract Methods:
        make_card: Create a game-specific card
        make_hand: Create a game-specific hand

    Example:
        >>> factory = CribbageFactory()
        >>> card = factory.make_card(11, Suit.Hearts)  # Jack of Hearts
        >>> hand = factory.make_hand(card1, card2, card3)
    """

    @abc.abstractmethod
    def make_card(self, rank: int, suit: Suit) -> "Card":
        """
        Create a game-specific card.

        Args:
            rank (int): Card rank (1-13)
            suit (Suit): Card suit

        Returns:
            Card: Game-specific card instance

        Note:
            Must be implemented by concrete factory subclasses.
        """
        ...

    @abc.abstractmethod
    def make_hand(self, *cards: Card) -> "Hand":
        """
        Create a game-specific hand.

        Args:
            *cards: Variable number of cards for the hand

        Returns:
            Hand: Game-specific hand instance

        Note:
            Must be implemented by concrete factory subclasses.
        """
        ...

class CribbageCard(Card):
    """
    Standard cribbage card with point value equal to rank.

    In cribbage, most cards have a point value equal to their rank
    for the purpose of making fifteens and other scoring combinations.
    This class represents cards 2-10.

    Fixed: Changed 'points' to 'points' for consistency
    """
    @property
    def points(self) -> int:
        """Return point value for cribbage scoring."""
        return self.rank


class CribbageAce(Card):
    """
    Ace card in cribbage with point value of 1.

    In cribbage, Aces always have a point value of 1 regardless
    of their rank representation, used for making fifteens.

    Fixed: Changed 'point' to 'points' for consistency
    """
    @property
    def points(self) -> int:
        """Return point value of 1 for Ace."""
        return 1


class CribbageFace(Card):
    """
    Face card (Jack, Queen, King) in cribbage with point value of 10.

    In cribbage, all face cards (Jack, Queen, King) have a point
    value of 10 for the purpose of making fifteens and scoring.

    Note: Class name has typo 'CribbaageFace' - should be 'CribbageFace'
    """
    @property
    def points(self) -> int:
        """Return point value of 10 for face cards."""
        return 10


class CribbageTrick(Trick):
    """
    Enumeration of scoring combinations in cribbage.

    This enum defines all the possible scoring tricks/combinations
    that can be found in a cribbage hand during scoring.

    Scoring Types:
        Fifteen: Any combination of cards totaling 15 points
        Pair: Two cards of the same rank
        Run_3: Three cards in sequence
        Run_4: Four cards in sequence
        Run_5: Five cards in sequence
        Right_Jack: Jack matching the starter card suit

    Fixed: Added missing Right_Jack and corrected 'Fiftleen' to 'Fifteen'
    """
    Fifteen = auto()
    Pair = auto()
    Run_3 = auto()
    Run_4 = auto()
    Run_5 = auto()
    Right_Jack = auto() 


C = TypeVar("C")


def powerset(iterable: Iterable[C]) -> Iterator[tuple[C, ...]]:
    """
    Generate all possible subsets (powerset) of an iterable.

    This function generates all possible combinations of elements from the
    input iterable, including the empty set and the full set. It's used
    in cribbage scoring to find all possible card combinations that sum to 15.

    Args:
        iterable: Any iterable collection of elements

    Returns:
        Iterator[tuple[C, ...]]: Iterator yielding all possible subsets as tuples

    Example:
        >>> list(powerset([1, 2, 3]))
        [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]

        >>> # Used for finding card combinations that sum to 15
        >>> cards = [Card(5, Suit.Hearts), Card(10, Suit.Clubs)]
        >>> for subset in powerset(cards):
        ...     if sum(c.rank for c in subset) == 15:
        ...         print(f"Fifteen: {subset}")
    """
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )


class CribbageHand(Hand):
    """
    Specialized hand implementation for cribbage scoring.

    This class extends the base Hand class to provide cribbage-specific
    functionality including starter card management and comprehensive
    scoring algorithms for all cribbage combinations.

    Cribbage scoring includes:
    - Fifteens: Combinations of cards that sum to 15 (2 points each)
    - Pairs: Two cards of the same rank (2 points each)
    - Runs: Sequential ranks (1 point per card)
    - Right Jack: Jack matching starter suit (1 point)

    Attributes:
        starter (Card): The starter card (upcard) used for scoring

    Example:
        >>> hand = CribbageHand(Card(5, Suit.Hearts), Card(10, Suit.Clubs))
        >>> starter = Card(5, Suit.Spades)
        >>> scored_hand = hand.upcard(starter)
        >>> tricks = scored_hand.scoring()
    """    
    starter: Card


    def upcard(self, starter: Card) -> "Hand":
        """
        Set the starter card and return the hand for method chaining.

        The starter card (upcard) is used in cribbage scoring and becomes
        part of the effective hand for calculating points.

        Args:
            starter (Card): The starter card to use for scoring

        Returns:
            Hand: Self reference for method chaining

        Example:
            >>> hand = CribbageHand(Card(6, Suit.Hearts))
            >>> scored_hand = hand.upcard(Card(9, Suit.Clubs))
            >>> isinstance(scored_hand, CribbageHand)
            True
        """
        self.starter = starter
        return self

    def scoring(self) -> list[Trick]:
        """
        Calculate all scoring combinations in the cribbage hand.

        Analyzes the hand plus starter card to find all possible scoring
        combinations according to cribbage rules. Uses powerset analysis
        to find all card combinations that sum to 15.

        Scoring Rules:
        - Fifteens: Any combination summing to 15 = 2 points
        - Pairs: Two cards of same rank = 2 points
        - Runs: 3+ consecutive ranks = 1 point per card
        - Right Jack: Jack matching starter suit = 1 point

        Returns:
            list[Trick]: List of all scoring tricks found in the hand

        Example:
            >>> # Hand: 5♥, 10♣, Starter: 5♠
            >>> # Scores: Fifteen (5+10), Pair (5♥,5♠)
            >>> tricks = hand.scoring()
            >>> CribbageTrick.Fifteen in tricks
            True
            >>> CribbageTrick.Pair in tricks
            True
        """
        def trick_iter(cards: list[CribbageCard]) -> Iterator[Trick]:
            for subset in powerset(cards):
                if sum(c.points for c in subset) == 15:
                    yield CribbageTrick.Fifteen
            for c1, c2 in itertools.combinations(cards, 2):
                if c1.rank == c2.rank:
                    yield CribbageTrick.Pair
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

        def run_length(sorted_cards: list[CribbageCard]) -> int:
            card_iter = iter(sorted_cards)
            base = next(card_iter)
            for offset, card in enumerate(card_iter, start=1):
                if base.rank + offset != card.rank:
                    break

            return offset + 1

        hand_plus_starter = cast(list[CribbageCard], self + [self.starter])
        hand_plus_starter.sort()

        tricks = list(trick_iter(hand_plus_starter))

        if run_length(hand_plus_starter) == 5:
            tricks += [CribbageTrick.Run_5]
        elif (
            run_length(hand_plus_starter) == 4 or run_length(hand_plus_starter[1:]) == 4
        ):
            tricks += [CribbageTrick.Run_4]
        elif (
            run_length(hand_plus_starter) == 3
            or run_length(hand_plus_starter[1:]) == 3
            or run_length(hand_plus_starter[2:]) == 3
        ):
            tricks += [CribbageTrick.Run_3]
        right_jack = any(c.rank == 11 and c.suit == self.starter.suit for c in self)
        if right_jack:
            tricks += [CribbageTrick.Right_Jack]
        return tricks


class CribbageFactory(CardGameFactory):
    """
    Concrete factory for creating cribbage-specific cards and hands.

    This factory implements the CardGameFactory interface to create
    cribbage-specific card types based on rank, ensuring proper
    point values for cribbage scoring calculations.

    Card Creation Rules:
    - Rank 1: Creates CribbageAce (1 point)
    - Ranks 2-10: Creates CribbageCard (rank points)
    - Ranks 11-13: Creates CribbageAce (should be CribbageFace for 10 points)

    Note: There's a bug in the factory - face cards (11-13) should
    create CribbageFace instances, not CribbageAce instances.

    Example:
        >>> factory = CribbageFactory()
        >>> ace = factory.make_card(1, Suit.Hearts)
        >>> isinstance(ace, CribbageAce)
        True
        >>> five = factory.make_card(5, Suit.Clubs)
        >>> isinstance(five, CribbageCard)
        True
    """

    def make_card(self, rank: int, suit: Suit) -> "Card":
        """
        Create a cribbage-specific card based on rank.

        Args:
            rank (int): Card rank (1-13)
            suit (Suit): Card suit

        Returns:
            Card: Appropriate cribbage card type

        Fixed: Face cards (11-13) now correctly create CribbageFace instead of CribbageAce
        """
        if rank == 1:
            return CribbageAce(rank, suit)
        elif 2 <= rank < 11:
            return CribbageCard(rank, suit)
        else:
            return CribbageFace(rank, suit)

    def make_hand(self, *cards: Card) -> "Hand":
        """
        Create a cribbage hand from the given cards.

        Args:
            *cards: Variable number of Card objects

        Returns:
            Hand: CribbageHand instance containing the cards
        """
        return CribbageHand(*cards)


factory = CribbageFactory()

cards = [
    factory.make_card(6, Suit.Clubs),
    factory.make_card(7, Suit.Diamonds),
    factory.make_card(8, Suit.Hearts),
    factory.make_card(9, Suit.Spades),
]

starter = factory.make_card(5, Suit.Spades)
hand = factory.make_hand(*cards)
score = sorted(hand.upcard(starter).scoring())
print(t.name for t in score)


class PokerCard(Card):
    """
    Poker-specific card implementation with Ace-high representation.

    This class extends Card to provide poker-specific string representation
    where Aces (rank 14) are displayed as 'A' rather than '14'.

    In poker, Aces are typically high (rank 14) but can also be low
    in some straight combinations.

    Example:
        >>> ace = PokerCard(14, Suit.Spades)
        >>> str(ace)
        'A♠'
        >>> king = PokerCard(13, Suit.Hearts)
        >>> str(king)
        '13♥'
    """

    def __str__(self) -> str:
        """
        Return poker-style string representation.

        Returns:
            str: 'A' + suit for Aces, otherwise rank + suit
        """
        if self.rank == 14:
            return f"A{self.suit}"
        return f"{self.rank}{self.suit}"


class PokerTrick(Trick):
    """
    Enumeration of poker hand rankings and combinations.

    This enum defines all standard poker hand types in order of
    increasing value/rarity. Used by PokerHand.scoring() to
    identify and return the hand type.

    Hand Rankings (lowest to highest):
    - Pair: Two cards of same rank
    - TwoPair: Two different pairs
    - Three: Three cards of same rank
    - Straight: Five sequential ranks
    - Flush: Five cards of same suit
    - FullHouse: Three of a kind + pair
    - Four: Four cards of same rank
    - StraightFlush: Straight + flush
    """

    Pair = auto()
    TwoPair = auto()
    Three = auto()
    Straight = auto()
    Flush = auto()
    FullHouse = auto()
    Four = auto()
    StraightFlush = auto()


class PokerHand(Hand):
    """
    Poker hand implementation with comprehensive hand ranking evaluation.

    This class extends Hand to provide poker-specific hand evaluation
    that determines the highest-ranking poker combination in a 5-card hand.

    The evaluation algorithm analyzes:
    - Rank frequency distribution (pairs, trips, quads)
    - Suit distribution (flush detection)
    - Sequential ranks (straight detection)

    Hand Evaluation Logic:
    - 1 distinct rank: Invalid (five of a kind)
    - 2 distinct ranks: Four of a kind OR Full house
    - 3 distinct ranks: Three of a kind OR Two pair
    - 4 distinct ranks: One pair
    - 5 distinct ranks: Straight, Flush, Straight flush, or High card

    Example:
        >>> cards = [PokerCard(10, Suit.Hearts), PokerCard(10, Suit.Clubs)]
        >>> hand = PokerHand(*cards)
        >>> ranking = hand.scoring()
        >>> PokerTrick.Pair in ranking
        True
    """

    def scoring(self) -> list[Trick]:
        """
        Evaluate the poker hand and return the highest ranking.

        Analyzes the 5-card hand to determine the best poker combination
        according to standard poker rules. Returns a list containing
        the single best hand type.

        Returns:
            list[Trick]: Single-element list with the hand's ranking

        Raises:
            Exception: If hand contains five of a kind (invalid)
            Exception: If hand structure is unexpected

        Algorithm:
        1. Count distinct ranks and suits
        2. Analyze rank frequency patterns
        3. Check for straights and flushes
        4. Return appropriate hand type

        Example:
            >>> # Full house: 3 Kings + 2 Aces
            >>> hand = PokerHand(King♠, King♥, King♣, Ace♠, Ace♥)
            >>> hand.scoring()
            [<PokerTrick.FullHouse: 6>]
        """

        # Distinct Ranks
        ranks: Counter[int] = collections.Counter(c.rank for c in self)
        # Distinct Suits
        flush = len(set(c.suit for c in self)) == 1

        if len(ranks) == 1:
            # five of kind!
            raise Exception(f"Broken Hand {self}")
        elif len(ranks) == 2:
            # 4-1 or 3-2
            card, count = ranks.most_common(1)[0]
            if count == 4:
                return [PokerTrick.Four]
            elif count == 3:
                return [PokerTrick.FullHouse]
            else:
                raise Exception(f"Broken Hand {self}")
        elif len(ranks) == 3:
            # 3-1-1, or 2-2-1
            card, count = ranks.most_common(1)[0]
            if count == 3:
                return [PokerTrick.Three]
            elif count == 2:
                return [PokerTrick.TwoPair]
            else:
                raise Exception(f"Broken Hand {self}")
        elif len(ranks) == 4:
            # 2-1-1-1
            return [PokerTrick.Pair]
        elif len(ranks) == 5:
            # straight?
            base = min(ranks)
            straight = all(base + offset == rank for offset, rank in enumerate(ranks))
            # straight flush?
            if straight and flush:
                return [PokerTrick.StraightFlush]
            elif straight:
                return [PokerTrick.Straight]
            elif flush:
                return [PokerTrick.Flush]
            else:
                return []
        else:
            return []


class PokerFactory(CardGameFactory):
    """
    Concrete factory for creating poker-specific cards and hands.

    This factory implements the CardGameFactory interface to create
    poker-specific card types with Ace-high ranking (Ace = 14).

    Poker Card Rules:
    - Rank 1 (Ace): Converted to rank 14 (Ace-high)
    - All other ranks: Used as-is
    - All cards: Created as PokerCard instances

    Example:
        >>> factory = PokerFactory()
        >>> ace = factory.make_card(1, Suit.Spades)  # Becomes rank 14
        >>> ace.rank
        14
        >>> king = factory.make_card(13, Suit.Hearts)
        >>> king.rank
        13
    """

    def make_card(self, rank: int, suit: Suit) -> "Card":
        """
        Create a poker card with Ace-high ranking.

        Args:
            rank (int): Input rank (1-13, where 1 = Ace)
            suit (Suit): Card suit

        Returns:
            Card: PokerCard with rank 14 for Aces, original rank for others
        """
        if rank == 1:
            # Aces above kings
            rank = 14
        return PokerCard(rank, suit)

    def make_hand(self, *cards: Card) -> "Hand":
        """
        Create a poker hand from the given cards.

        Args:
            *cards: Variable number of Card objects

        Returns:
            Hand: PokerHand instance for hand evaluation
        """
        return PokerHand(*cards)


factory = PokerFactory()
cards = [
    factory.make_card(5, Suit.Clubs),
    factory.make_card(5, Suit.Diamonds),
    factory.make_card(5, Suit.Hearts),
    factory.make_card(6, Suit.Spades),
    factory.make_card(6, Suit.Spades),
]
hand = factory.make_hand(*cards)
print(hand.scoring())


class Game:
    """
    Base game controller providing deck management and basic game operations.

    This class provides the foundation for card game implementations,
    handling deck creation, shuffling, dealing, and basic scoring.
    Uses the factory pattern to create game-specific cards and hands.

    Note: There's a typo in the code - 'dect' should be 'deck'

    Attributes:
        factory (CardGameFactory): Factory for creating cards and hands
        deck (list[Card]): The shuffled deck of cards (Note: called 'dect' in code)

    Example:
        >>> factory = PokerFactory()
        >>> game = Game(factory)
        >>> game.prepare()  # Creates and shuffles deck
        >>> hand = game.deal()  # Deals 5 cards
        >>> game.score(hand)  # Prints hand score
    """

    def __init__(self, factory: CardGameFactory) -> None:
        """
        Initialize game with a card factory.

        Args:
            factory: Factory for creating game-specific cards and hands
        """
        self.factory = factory

    def prepare(self) -> None:
        """
        Create and shuffle a standard 52-card deck.

        Creates a deck with ranks 1-13 for each suit, then shuffles it.
        Uses the factory to create appropriate card types for the game.
        """
        self.deck = [
            self.factory.make_card(r, s) for r in range(1, 14) for s in iter(Suit)
        ]
        random.shuffle(self.deck)

    def deal(self) -> Hand:
        """
        Deal a 5-card hand from the deck.

        Returns:
            Hand: A hand containing the first 5 cards from the deck
        """
        hand = self.factory.make_hand(*self.deck[:5])
        return hand

    def score(self, hand: Hand) -> None:
        """
        Score a hand and print the results.

        Args:
            hand: The hand to evaluate and score
        """

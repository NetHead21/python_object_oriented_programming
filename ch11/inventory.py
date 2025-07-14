"""
Zonk Game Observer Pattern Implementation

This module demonstrates the Observer pattern through a dice game called Zonk.
The implementation includes:
- Observer/Observable pattern for game state notifications
- ZonkHandHistory to track player dice rolls
- Specialized observers for game events (saving hands, detecting patterns)

The Observer pattern allows for loose coupling between the game state (Observable)
and various response mechanisms (Observers) that react to state changes.

Example:
    >>> from dice import Dice
    >>> player_dice = Dice(6, 6)  # 6 dice, 6 sides each
    >>> hand = ZonkHandHistory("Alice", player_dice)
    >>> save_observer = SaveZonkHand(hand)
    >>> pattern_observer = ThreePairZonkHand(hand)
    >>> hand.attach(save_observer)
    >>> hand.attach(pattern_observer)
    >>> hand.start()  # Triggers observers on first roll
    >>> hand.roll()   # Triggers observers on subsequent rolls

Date: July 14, 2025
"""

import json
import time
from dice import Dice
from typing import Protocol


class Observer(Protocol):
    """Protocol defining the interface for Observer pattern participants.

    This protocol ensures that all observers implement the required callback
    method that will be invoked when the observable object's state changes.

    The Observer pattern allows for one-to-many dependency relationships
    between objects, where when one object changes state, all dependents
    are notified automatically.
    """

    def __call__(self) -> None:
        """Observer callback method invoked when observable state changes.

        This method is called by the Observable object whenever its state
        changes and observers need to be notified. Observers should implement
        this method to define their response to state changes.

        Note:
            This method should not raise exceptions as it could disrupt
            the notification chain to other observers.
        """
        pass


class Observable:
    """Base class implementing the Observable part of the Observer pattern.

    This class maintains a list of observers and provides methods to attach,
    detach, and notify observers when state changes occur. Classes that extend
    Observable can trigger notifications to all registered observers.

    The Observable pattern is useful when:
    - Multiple objects need to react to state changes in another object
    - You want to maintain loose coupling between objects
    - The number of dependent objects may change at runtime

    Attributes:
        _observers (list[Observer]): List of registered observer objects

    Example:
        >>> observable = Observable()
        >>> observer1 = MyObserver()
        >>> observer2 = AnotherObserver()
        >>> observable.attach(observer1)
        >>> observable.attach(observer2)
        >>> observable._notify_observers()  # Both observers called
    """

    def __init__(self):
        """Initialize Observable with empty observer list."""
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Register an observer to receive state change notifications.

        Args:
            observer (Observer): The observer object to register. Must implement
                the Observer protocol (callable with no arguments).

        Note:
            The same observer can be attached multiple times, which will
            result in multiple notifications for each state change.
        """
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Remove an observer from the notification list.

        Args:
            observer (Observer): The observer object to remove.

        Raises:
            ValueError: If the observer is not in the list.

        Note:
            Only removes the first occurrence if the observer was
            attached multiple times.
        """
        self._observers.remove(observer)

    def _notify_observers(self) -> None:
        """Notify all registered observers of a state change.

        Calls each observer's __call__ method in the order they were attached.
        If an observer raises an exception, it's caught and logged, but
        notification continues to other observers.

        Note:
            This is typically called by subclasses when their state changes.
        """
        for observer in self._observers:
            try:
                observer()
            except Exception as e:
                # In a production system, you'd want proper logging here
                print(f"Warning: Observer {observer} raised exception: {e}")


Hand = list[int]  # Type alias for clarity - represents a dice roll result


class ZonkHandHistory(Observable):
    """Tracks the history of dice rolls for a Zonk game player.

    This class extends Observable to notify observers whenever new dice
    rolls occur. It maintains a complete history of all rolls made by
    a player during their turn, allowing observers to analyze patterns
    and react to game events.

    Zonk is a dice game where players roll dice and try to score points
    based on various combinations. This class specifically tracks the
    sequence of rolls to enable pattern detection and game state management.

    Attributes:
        player (str): Name of the player whose rolls are being tracked
        dice_set (Dice): The dice object used for rolling
        rolls (list[Hand]): Complete history of all dice rolls made

    Example:
        >>> from dice import Dice
        >>> dice = Dice(6, 6)  # 6 dice, 6 sides each
        >>> hand = ZonkHandHistory("Alice", dice)
        >>> first_roll = hand.start()  # Start tracking and make first roll
        >>> second_roll = hand.roll()  # Make additional rolls
    """

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
    def __call__(self) -> None:
        pass

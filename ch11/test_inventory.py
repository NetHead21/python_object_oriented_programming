"""
Test suite for the Zonk Game Observer Pattern Implementation

This module provides comprehensive tests for the observer pattern implementation
in the inventory.py module. It includes unit tests for all classes and
integration tests demonstrating the complete observer pattern workflow.

Run with: python -m pytest test_inventory.py -v
Or simply: python test_inventory.py

Author: Workshop Instructor
Date: July 14, 2025
"""

import unittest
from unittest.mock import patch
import json
import time
from inventory import Observable, ZonkHandHistory, SaveZonkHand, ThreePairZonkHand


class MockDice:
    """Mock Dice class for testing without external dependencies."""

    def __init__(self, count=6, sides=6):
        self.count = count
        self.sides = sides
        self.dice = [1] * count  # Default roll

    def roll(self):
        """Mock roll - can be controlled in tests."""
        pass


class MockObserver:
    """Simple mock observer for testing Observable functionality."""

    def __init__(self):
        self.call_count = 0
        self.last_called = None

    def __call__(self):
        self.call_count += 1
        self.last_called = time.time()


class TestObservable(unittest.TestCase):
    """Test cases for the Observable base class."""

    def setUp(self):
        self.observable = Observable()
        self.observer1 = MockObserver()
        self.observer2 = MockObserver()

    def test_attach_observer(self):
        """Test attaching observers to observable."""
        self.observable.attach(self.observer1)
        self.assertEqual(len(self.observable._observers), 1)

        self.observable.attach(self.observer2)
        self.assertEqual(len(self.observable._observers), 2)

    def test_detach_observer(self):
        """Test detaching observers from observable."""
        self.observable.attach(self.observer1)
        self.observable.attach(self.observer2)

        self.observable.detach(self.observer1)
        self.assertEqual(len(self.observable._observers), 1)
        self.assertIn(self.observer2, self.observable._observers)
        self.assertNotIn(self.observer1, self.observable._observers)

    def test_detach_nonexistent_observer(self):
        """Test that detaching non-existent observer raises ValueError."""
        with self.assertRaises(ValueError):
            self.observable.detach(self.observer1)

    def test_notify_observers(self):
        """Test that all attached observers are notified."""
        self.observable.attach(self.observer1)
        self.observable.attach(self.observer2)

        self.observable._notify_observers()

        self.assertEqual(self.observer1.call_count, 1)
        self.assertEqual(self.observer2.call_count, 1)

    def test_notify_observers_with_exception(self):
        """Test that exceptions in observers don't stop other notifications."""

        def failing_observer():
            raise RuntimeError("Observer error")

        self.observable.attach(failing_observer)
        self.observable.attach(self.observer1)

        # Should not raise exception despite failing observer
        with patch("builtins.print") as mock_print:
            self.observable._notify_observers()

        # Verify that the non-failing observer was still called
        self.assertEqual(self.observer1.call_count, 1)
        # Verify error was logged
        mock_print.assert_called()


class TestZonkHandHistory(unittest.TestCase):
    """Test cases for ZonkHandHistory class."""

    def setUp(self):
        self.mock_dice = MockDice()
        self.hand = ZonkHandHistory("TestPlayer", self.mock_dice)
        self.observer = MockObserver()

    def test_initialization(self):
        """Test proper initialization of ZonkHandHistory."""
        self.assertEqual(self.hand.player, "TestPlayer")
        self.assertEqual(self.hand.dice_set, self.mock_dice)
        self.assertEqual(self.hand.rolls, [])

    def test_start_method(self):
        """Test the start method creates initial roll and notifies observers."""
        self.mock_dice.dice = [1, 2, 3, 4, 5, 6]
        self.hand.attach(self.observer)

        result = self.hand.start()

        self.assertEqual(result, [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(self.hand.rolls), 1)
        self.assertEqual(self.hand.rolls[0], [1, 2, 3, 4, 5, 6])
        self.assertEqual(self.observer.call_count, 1)

    def test_roll_method(self):
        """Test the roll method adds to history and notifies observers."""
        # Setup initial state
        self.mock_dice.dice = [1, 1, 1, 1, 1, 1]
        self.hand.start()
        self.hand.attach(self.observer)

        # Make additional roll
        self.mock_dice.dice = [6, 6, 6, 6, 6, 6]
        result = self.hand.roll()

        self.assertEqual(result, [6, 6, 6, 6, 6, 6])
        self.assertEqual(len(self.hand.rolls), 2)
        self.assertEqual(self.hand.rolls[1], [6, 6, 6, 6, 6, 6])
        self.assertEqual(self.observer.call_count, 1)  # Only counting after attach

    def test_multiple_rolls(self):
        """Test multiple rolls build proper history."""
        rolls_sequence = [[1, 2, 3, 4, 5, 6], [2, 2, 2, 2, 2, 2], [3, 3, 4, 4, 5, 5]]

        for i, roll in enumerate(rolls_sequence):
            self.mock_dice.dice = roll
            if i == 0:
                self.hand.start()
            else:
                self.hand.roll()

        self.assertEqual(len(self.hand.rolls), 3)
        self.assertEqual(self.hand.rolls, rolls_sequence)


class TestSaveZonkHand(unittest.TestCase):
    """Test cases for SaveZonkHand observer."""

    def setUp(self):
        self.mock_dice = MockDice()
        self.hand = ZonkHandHistory("TestPlayer", self.mock_dice)
        self.save_observer = SaveZonkHand(self.hand)

    def test_initialization(self):
        """Test proper initialization of SaveZonkHand."""
        self.assertEqual(self.save_observer.hand, self.hand)
        self.assertEqual(self.save_observer.count, 0)

    @patch("builtins.print")
    @patch("time.time", return_value=1234567890.0)
    def test_save_observer_call(self, mock_time, mock_print):
        """Test that SaveZonkHand creates proper log messages."""
        self.hand.rolls = [[1, 2, 3, 4, 5, 6]]

        self.save_observer()

        expected_message = {
            "player": "TestPlayer",
            "sequence": 1,
            "hand": json.dumps([[1, 2, 3, 4, 5, 6]]),
            "time": 1234567890.0,
        }

        self.assertEqual(self.save_observer.count, 1)
        mock_print.assert_called_once_with(f"SaveZonkHand: {expected_message}")

    @patch("builtins.print")
    def test_multiple_saves_increment_sequence(self, mock_print):
        """Test that sequence number increments with each save."""
        self.hand.rolls = [[1, 2, 3, 4, 5, 6]]

        self.save_observer()
        self.save_observer()
        self.save_observer()

        self.assertEqual(self.save_observer.count, 3)
        self.assertEqual(mock_print.call_count, 3)


class TestThreePairZonkHand(unittest.TestCase):
    """Test cases for ThreePairZonkHand observer."""

    def setUp(self):
        self.mock_dice = MockDice()
        self.hand = ZonkHandHistory("TestPlayer", self.mock_dice)
        self.pattern_observer = ThreePairZonkHand(self.hand)

    def test_initialization(self):
        """Test proper initialization of ThreePairZonkHand."""
        self.assertEqual(self.pattern_observer.hand, self.hand)
        self.assertFalse(self.pattern_observer.zonked)

    @patch("builtins.print")
    def test_three_pair_detection_positive(self, mock_print):
        """Test detection of valid three-pair patterns."""
        # Valid three-pair patterns
        three_pair_patterns = [
            [1, 1, 2, 2, 3, 3],
            [2, 2, 4, 4, 6, 6],
            [1, 3, 1, 5, 3, 5],  # Order doesn't matter
        ]

        for pattern in three_pair_patterns:
            with self.subTest(pattern=pattern):
                self.hand.rolls = [pattern]
                self.pattern_observer()

                self.assertTrue(self.pattern_observer.zonked)
                mock_print.assert_called()

                # Reset for next test
                self.pattern_observer.zonked = False
                mock_print.reset_mock()

    def test_three_pair_detection_negative(self):
        """Test that non-three-pair patterns are not detected."""
        # Invalid patterns
        non_three_pair_patterns = [
            [1, 1, 1, 1, 1, 1],  # All same
            [1, 2, 3, 4, 5, 6],  # All different
            [1, 1, 1, 2, 2, 2],  # Two triples
            [1, 1, 2, 2, 3, 4],  # Two pairs + two singles
            [1, 1, 1, 2, 2, 3],  # One triple + one pair + one single
        ]

        for pattern in non_three_pair_patterns:
            with self.subTest(pattern=pattern):
                self.hand.rolls = [pattern]
                self.pattern_observer()

                self.assertFalse(self.pattern_observer.zonked)

    def test_empty_rolls_handling(self):
        """Test handling of empty rolls list."""
        self.hand.rolls = []
        self.pattern_observer()

        self.assertFalse(self.pattern_observer.zonked)

    @patch("builtins.print")
    def test_zonk_message_format(self, mock_print):
        """Test the format of the zonk detection message."""
        self.hand.rolls = [[3, 1, 3, 2, 1, 2]]  # Three pairs: 1,1,2,2,3,3

        self.pattern_observer()

        # Should print message with sorted roll for clarity
        mock_print.assert_called_once_with("3 Pair Zonk! Roll: [1, 1, 2, 2, 3, 3]")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete observer pattern system."""

    def setUp(self):
        self.mock_dice = MockDice()
        self.hand = ZonkHandHistory("IntegrationTestPlayer", self.mock_dice)
        self.save_observer = SaveZonkHand(self.hand)
        self.pattern_observer = ThreePairZonkHand(self.hand)

    @patch("builtins.print")
    @patch("time.time", return_value=1234567890.0)
    def test_complete_workflow(self, mock_time, mock_print):
        """Test complete workflow with multiple observers."""
        # Attach both observers
        self.hand.attach(self.save_observer)
        self.hand.attach(self.pattern_observer)

        # First roll - not a three-pair
        self.mock_dice.dice = [1, 2, 3, 4, 5, 6]
        self.hand.start()

        # Second roll - three pairs
        self.mock_dice.dice = [2, 2, 4, 4, 6, 6]
        self.hand.roll()

        # Verify both observers were called twice
        self.assertEqual(self.save_observer.count, 2)
        self.assertTrue(self.pattern_observer.zonked)

        # Verify print was called for both save operations and zonk detection
        self.assertEqual(mock_print.call_count, 3)  # 2 saves + 1 zonk message

    def test_observer_independence(self):
        """Test that observers operate independently."""
        self.hand.attach(self.save_observer)
        self.hand.attach(self.pattern_observer)

        # Remove pattern observer
        self.hand.detach(self.pattern_observer)

        # Roll should only trigger save observer
        self.mock_dice.dice = [1, 1, 2, 2, 3, 3]  # Three pairs
        self.hand.start()

        self.assertEqual(self.save_observer.count, 1)
        self.assertFalse(self.pattern_observer.zonked)  # Wasn't called

    def test_multiple_players(self):
        """Test system with multiple players and observers."""
        # Create second player
        mock_dice2 = MockDice()
        hand2 = ZonkHandHistory("Player2", mock_dice2)
        save_observer2 = SaveZonkHand(hand2)

        # Setup observers
        self.hand.attach(self.save_observer)
        hand2.attach(save_observer2)

        # Both players roll
        self.mock_dice.dice = [1, 2, 3, 4, 5, 6]
        mock_dice2.dice = [6, 5, 4, 3, 2, 1]

        self.hand.start()
        hand2.start()

        # Verify independent tracking
        self.assertEqual(self.save_observer.count, 1)
        self.assertEqual(save_observer2.count, 1)
        self.assertEqual(len(self.hand.rolls), 1)
        self.assertEqual(len(hand2.rolls), 1)


def demonstrate_usage():
    """Demonstrate the complete Zonk observer system."""
    print("\n" + "=" * 60)
    print("ZONK GAME OBSERVER PATTERN DEMONSTRATION")
    print("=" * 60)

    # Create mock dice for demonstration
    dice = MockDice(6, 6)

    # Create hand for player
    hand = ZonkHandHistory("DemoPlayer", dice)

    # Create observers
    save_observer = SaveZonkHand(hand)
    pattern_observer = ThreePairZonkHand(hand)

    # Attach observers
    hand.attach(save_observer)
    hand.attach(pattern_observer)

    print(f"\nPlayer: {hand.player}")
    print("Attached observers: SaveZonkHand, ThreePairZonkHand")

    # Simulate game sequence
    rolls_sequence = [
        [1, 2, 3, 4, 5, 6],  # Normal roll
        [1, 1, 2, 3, 4, 5],  # Pair
        [2, 2, 4, 4, 6, 6],  # Three pairs - ZONK!
    ]

    for i, roll in enumerate(rolls_sequence):
        print(f"\n--- Roll {i + 1} ---")
        dice.dice = roll

        if i == 0:
            result = hand.start()
            print(f"Started game with roll: {result}")
        else:
            result = hand.roll()
            print(f"Rolled: {result}")

        print(f"Pattern observer zonked: {pattern_observer.zonked}")

    print(f"\nTotal rolls recorded: {len(hand.rolls)}")
    print(f"Save observer call count: {save_observer.count}")
    print("\nDemonstration complete!")


if __name__ == "__main__":
    # Run demonstration
    demonstrate_usage()

    # Run tests
    print("\n" + "=" * 60)
    print("RUNNING UNIT TESTS")
    print("=" * 60)
    unittest.main(verbosity=2)

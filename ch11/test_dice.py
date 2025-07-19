"""
Comprehensive Test Suite for Advanced Dice Rolling System

This test suite validates all functionality of the improved dice.py module,
including basic rolling, adjustments, text parsing, error handling, and
edge cases.

Run with: python -m pytest test_dice.py -v
Or simply: python test_dice.py

Author: Workshop Instructor
Date: July 14, 2025
"""

import unittest
from unittest.mock import patch
from dice import (
    Dice,
    Roll,
    Drop,
    Keep,
    Plus,
    Minus,
    DiceType,
    DiceError,
    InvalidDiceNotation,
    InvalidAdjustment,
    roll_basic,
    advantage,
    disadvantage,
    ability_score,
    dice_roller,
    d4,
    d6,
    d8,
    d10,
    d12,
    d20,
    d100,
)


class TestDiceTypes(unittest.TestCase):
    """Test the DiceType enumeration."""

    def test_dice_type_values(self):
        """Test that dice types have correct values."""
        self.assertEqual(DiceType.D4, 4)
        self.assertEqual(DiceType.D6, 6)
        self.assertEqual(DiceType.D8, 8)
        self.assertEqual(DiceType.D10, 10)
        self.assertEqual(DiceType.D12, 12)
        self.assertEqual(DiceType.D20, 20)
        self.assertEqual(DiceType.D100, 100)


class TestAdjustments(unittest.TestCase):
    """Test individual adjustment classes."""

    def setUp(self):
        self.dice = Dice(3, 6)
        self.dice.dice = [1, 3, 5]  # Known values for testing
        self.dice.modifier = 0

    def test_adjustment_negative_amount(self):
        """Test that negative amounts raise ValueError."""
        with self.assertRaises(ValueError):
            Drop(-1)

    def test_roll_adjustment(self):
        """Test the Roll adjustment."""
        roll_adj = Roll(2, 8)
        with patch("random.randint", side_effect=[3, 7]):
            roll_adj.apply(self.dice)
        self.assertEqual(self.dice.dice, [3, 7])
        self.assertEqual(self.dice.modifier, 0)

    def test_roll_invalid_parameters(self):
        """Test Roll with invalid parameters."""
        with self.assertRaises(ValueError):
            Roll(0, 6)
        with self.assertRaises(ValueError):
            Roll(3, 0)

    def test_drop_adjustment(self):
        """Test the Drop adjustment."""
        drop_adj = Drop(1)
        drop_adj.apply(self.dice)
        self.assertEqual(self.dice.dice, [3, 5])  # Dropped lowest (1)

    def test_drop_too_many(self):
        """Test dropping more dice than available."""
        drop_adj = Drop(5)  # More than 3 dice
        with self.assertRaises(InvalidAdjustment):
            drop_adj.apply(self.dice)

    def test_keep_adjustment(self):
        """Test the Keep adjustment."""
        keep_adj = Keep(2)
        keep_adj.apply(self.dice)
        self.assertEqual(self.dice.dice, [3, 5])  # Kept highest 2

    def test_keep_too_many(self):
        """Test keeping more dice than available."""
        keep_adj = Keep(5)  # More than 3 dice
        with self.assertRaises(InvalidAdjustment):
            keep_adj.apply(self.dice)

    def test_plus_adjustment(self):
        """Test the Plus adjustment."""
        plus_adj = Plus(3)
        plus_adj.apply(self.dice)
        self.assertEqual(self.dice.modifier, 3)

    def test_minus_adjustment(self):
        """Test the Minus adjustment."""
        minus_adj = Minus(2)
        minus_adj.apply(self.dice)
        self.assertEqual(self.dice.modifier, -2)

    def test_adjustment_repr(self):
        """Test string representations of adjustments."""
        self.assertEqual(repr(Drop(1)), "Drop(1)")
        self.assertEqual(repr(Plus(5)), "Plus(5)")
        self.assertEqual(repr(Roll(3, 6)), "Roll(3d6)")


class TestDiceClass(unittest.TestCase):
    """Test the main Dice class."""

    def test_dice_initialization(self):
        """Test proper initialization of Dice objects."""
        dice = Dice(3, 6)
        self.assertEqual(len(dice.adjustments), 1)  # Just the Roll
        self.assertIsInstance(dice.adjustments[0], Roll)

    def test_dice_invalid_parameters(self):
        """Test Dice with invalid parameters."""
        with self.assertRaises(ValueError):
            Dice(0, 6)
        with self.assertRaises(ValueError):
            Dice(3, 0)

    def test_dice_with_adjustments(self):
        """Test Dice with multiple adjustments."""
        dice = Dice(4, 6, Drop(1), Plus(2))
        self.assertEqual(len(dice.adjustments), 3)  # Roll + Drop + Plus

    def test_roll_method(self):
        """Test the roll method returns proper values."""
        dice = Dice(1, 6)

        # Mock the random roll to get predictable results
        with patch("random.randint", return_value=4):
            result = dice.roll()
            self.assertEqual(result, 4)
            self.assertEqual(dice.dice, [4])
            self.assertEqual(dice.modifier, 0)

    def test_roll_with_adjustments(self):
        """Test rolling with complex adjustments."""
        dice = Dice(4, 6, Drop(1), Plus(3))

        # Mock random to return [1, 2, 3, 4], drop 1, keep [2, 3, 4], +3
        with patch("random.randint", side_effect=[1, 2, 3, 4]):
            result = dice.roll()
            self.assertEqual(result, 12)  # 2+3+4+3 = 12
            self.assertEqual(dice.dice, [2, 3, 4])
            self.assertEqual(dice.modifier, 3)

    def test_get_details(self):
        """Test the get_details method."""
        dice = Dice(2, 6, Plus(1))
        with patch("random.randint", side_effect=[3, 5]):
            dice.roll()
            details = dice.get_details()

            expected = {
                "individual_dice": [3, 5],
                "modifier": 1,
                "total": 9,
                "adjustments": ["Plus(1)"],
            }
            self.assertEqual(details, expected)

    def test_string_representations(self):
        """Test string representations of Dice objects."""
        dice = Dice(3, 6, Drop(1), Plus(2))
        self.assertEqual(str(dice), "3d6d1+2")
        self.assertIn("Dice(3, 6", repr(dice))


class TestDiceNotationParsing(unittest.TestCase):
    """Test parsing of dice notation strings."""

    def test_basic_notation(self):
        """Test basic dice notation parsing."""
        test_cases = [
            ("1d6", 1, 6, []),
            ("d20", 1, 20, []),
            ("3d8", 3, 8, []),
            ("2d12", 2, 12, []),
        ]

        for notation, expected_n, expected_d, expected_adj in test_cases:
            with self.subTest(notation=notation):
                dice = Dice.from_text(notation)
                roll_adj = dice.adjustments[0]
                self.assertEqual(roll_adj.n, expected_n)
                self.assertEqual(roll_adj.d, expected_d)
                self.assertEqual(len(dice.adjustments) - 1, len(expected_adj))

    def test_notation_with_adjustments(self):
        """Test notation with various adjustments."""
        test_cases = [
            ("3d6+2", Plus, 2),
            ("1d20-1", Minus, 1),
            ("4d6d1", Drop, 1),
            ("4d6k3", Keep, 3),
        ]

        for notation, adj_type, adj_amount in test_cases:
            with self.subTest(notation=notation):
                dice = Dice.from_text(notation)
                adjustment = dice.adjustments[1]  # Skip Roll
                self.assertIsInstance(adjustment, adj_type)
                self.assertEqual(adjustment.amount, adj_amount)

    def test_complex_notation(self):
        """Test complex notation with multiple adjustments."""
        dice = Dice.from_text("4d6d1+2")
        self.assertEqual(len(dice.adjustments), 3)  # Roll + Drop + Plus
        self.assertIsInstance(dice.adjustments[1], Drop)
        self.assertIsInstance(dice.adjustments[2], Plus)

    def test_invalid_notation(self):
        """Test that invalid notation raises appropriate errors."""
        invalid_notations = [
            "invalid",
            "3x6",
            "d",
            "3d",
            "",
            "0d6",
            "3d0",
            "3d6x2",
        ]

        for notation in invalid_notations:
            with self.subTest(notation=notation):
                with self.assertRaises(InvalidDiceNotation):
                    Dice.from_text(notation)

    def test_case_insensitive_parsing(self):
        """Test that parsing is case insensitive."""
        dice1 = Dice.from_text("3D6K2")
        dice2 = Dice.from_text("3d6k2")
        self.assertEqual(str(dice1), str(dice2))


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions and presets."""

    def test_roll_basic(self):
        """Test the roll_basic function."""
        with patch("random.randint", side_effect=[1, 3, 5]):
            result = roll_basic(3, 6)
            self.assertEqual(result, [1, 3, 5])

    def test_roll_basic_invalid(self):
        """Test roll_basic with invalid parameters."""
        with self.assertRaises(ValueError):
            roll_basic(0, 6)
        with self.assertRaises(ValueError):
            roll_basic(3, 0)

    def test_advantage(self):
        """Test advantage function."""
        adv_dice = advantage()
        self.assertEqual(len(adv_dice.adjustments), 2)  # Roll + Keep
        self.assertIsInstance(adv_dice.adjustments[1], Keep)
        self.assertEqual(adv_dice.adjustments[1].amount, 1)

    def test_disadvantage(self):
        """Test disadvantage function."""
        disadv_dice = disadvantage()
        self.assertEqual(len(disadv_dice.adjustments), 2)  # Roll + Drop
        self.assertIsInstance(disadv_dice.adjustments[1], Drop)
        self.assertEqual(disadv_dice.adjustments[1].amount, 1)

    def test_ability_score(self):
        """Test ability score generation."""
        ability_dice = ability_score()
        roll_adj = ability_dice.adjustments[0]
        drop_adj = ability_dice.adjustments[1]

        self.assertEqual(roll_adj.n, 4)
        self.assertEqual(roll_adj.d, 6)
        self.assertIsInstance(drop_adj, Drop)
        self.assertEqual(drop_adj.amount, 1)

    def test_convenience_dice_functions(self):
        """Test individual dice type convenience functions."""
        test_functions = [
            (d4, 4),
            (d6, 6),
            (d8, 8),
            (d10, 10),
            (d12, 12),
            (d20, 20),
            (d100, 100),
        ]

        for func, expected_sides in test_functions:
            with self.subTest(func=func.__name__):
                dice = func(2)  # Roll 2 dice
                roll_adj = dice.adjustments[0]
                self.assertEqual(roll_adj.n, 2)
                self.assertEqual(roll_adj.d, expected_sides)


class TestDiceRoller(unittest.TestCase):
    """Test the dice_roller network function."""

    def test_dice_roller_with_notation(self):
        """Test dice_roller with valid notation."""
        with patch("random.randint", side_effect=[3, 4, 5]):
            request = b"3d6+2"
            response = dice_roller(request)
            response_text = response.decode("utf-8")

            self.assertIn("3d6+2", response_text)
            self.assertIn("[3, 4, 5]", response_text)
            self.assertIn("+2", response_text)
            self.assertIn("= 14", response_text)

    def test_dice_roller_fallback(self):
        """Test dice_roller fallback for invalid notation."""
        with patch("dice.roll_basic", return_value=[1, 2, 3, 4, 5, 6]):
            request = b"invalid notation"
            response = dice_roller(request)
            response_text = response.decode("utf-8")

            self.assertIn("invalid notation", response_text)
            self.assertIn("[1, 2, 3, 4, 5, 6]", response_text)

    def test_dice_roller_unicode_error(self):
        """Test dice_roller with invalid UTF-8."""
        request = b"\xff\xfe"  # Invalid UTF-8
        response = dice_roller(request)
        response_text = response.decode("utf-8")

        self.assertIn("Error: Invalid UTF-8", response_text)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""

    def test_dice_error_hierarchy(self):
        """Test that custom exceptions have proper hierarchy."""
        self.assertTrue(issubclass(InvalidDiceNotation, DiceError))
        self.assertTrue(issubclass(InvalidAdjustment, DiceError))
        self.assertTrue(issubclass(DiceError, Exception))

    def test_invalid_adjustment_during_roll(self):
        """Test handling of invalid adjustments during rolling."""
        dice = Dice(2, 6, Drop(5))  # Try to drop more than available
        with self.assertRaises(InvalidAdjustment):
            dice.roll()


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""

    def test_complete_character_generation(self):
        """Test complete D&D character stat generation."""
        stats = []

        # Generate 6 ability scores
        for _ in range(6):
            score_dice = ability_score()
            with patch("random.randint", side_effect=[6, 5, 4, 3]):  # Drop the 3
                score = score_dice.roll()
                stats.append(score)

        # Should have 6 scores, each between 3-18
        self.assertEqual(len(stats), 6)
        for score in stats:
            self.assertGreaterEqual(score, 3)
            self.assertLessEqual(score, 18)

    def test_combat_simulation(self):
        """Test a simple combat simulation."""
        # Attack roll: 1d20+5
        attack = Dice.from_text("1d20+5")
        # Damage roll: 2d6+3
        damage = Dice.from_text("2d6+3")

        with patch("random.randint", side_effect=[15, 4, 2]):  # Attack 20, damage 9
            attack_result = attack.roll()
            damage_result = damage.roll()

        self.assertEqual(attack_result, 20)  # 15+5
        self.assertEqual(damage_result, 9)  # 4+2+3

    def test_advantage_vs_normal(self):
        """Test that advantage generally produces higher results."""
        # This is a statistical test, so we'll run many iterations
        normal_total = 0
        advantage_total = 0
        iterations = 100

        for _ in range(iterations):
            normal_dice = Dice(1, 20)
            adv_dice = advantage()

            normal_total += normal_dice.roll()
            advantage_total += adv_dice.roll()

        # Advantage should generally be higher than normal
        # (This might occasionally fail due to randomness, but very rarely)
        self.assertGreater(advantage_total, normal_total)


def demonstrate_usage():
    """Demonstrate the improved dice system capabilities."""
    print("\n" + "=" * 60)
    print("ADVANCED DICE SYSTEM DEMONSTRATION")
    print("=" * 60)

    print("\n1. Basic Dice Rolling:")
    basic = Dice(3, 6)
    result = basic.roll()
    print(f"3d6: {result}")
    print(f"Details: {basic.get_details()}")

    print("\n2. Complex Adjustments:")
    complex_dice = Dice(4, 6, Drop(1), Plus(2))
    result = complex_dice.roll()
    print(f"4d6 drop lowest +2: {result}")
    print(f"String representation: {complex_dice}")

    print("\n3. Text Notation Parsing:")
    notations = ["1d20+5", "3d6", "4d6k3", "2d8-1"]
    for notation in notations:
        dice = Dice.from_text(notation)
        result = dice.roll()
        print(f"{notation}: {result}")

    print("\n4. RPG Systems:")
    print("Ability Scores (4d6 drop lowest):")
    abilities = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    for ability in abilities:
        score = ability_score().roll()
        modifier = (score - 10) // 2
        sign = "+" if modifier >= 0 else ""
        print(f"  {ability}: {score:2d} ({sign}{modifier})")

    print("\nAdvantage vs Normal vs Disadvantage:")
    normal = Dice(1, 20)
    adv = advantage()
    disadv = disadvantage()

    print(f"  Normal: {normal.roll()}")
    print(f"  Advantage: {adv.roll()}")
    print(f"  Disadvantage: {disadv.roll()}")

    print("\n5. Convenience Functions:")
    dice_types = [d4, d6, d8, d10, d12, d20, d100]
    for dice_func in dice_types:
        dice = dice_func(2)  # Roll 2 of each type
        result = dice.roll()
        print(f"  2{dice_func.__name__}: {result}")

    print("\n6. Network Function:")
    test_requests = [b"3d6+2", b"1d20", b"invalid"]
    for request in test_requests:
        response = dice_roller(request)
        print(f"  Request: {request}")
        print(f"  Response: {response.decode()}")

    print("\nDemonstration complete!")


if __name__ == "__main__":
    # Run demonstration first
    demonstrate_usage()

    # Then run tests
    print("\n" + "=" * 60)
    print("RUNNING UNIT TESTS")
    print("=" * 60)
    unittest.main(verbosity=2, exit=False)

"""Vigenère cipher implementation with multiple versions demonstrating refactoring.

This module implements the Vigenère cipher, a method of encrypting alphabetic text
using a simple form of polyalphabetic substitution. The cipher uses a keyword to
shift each letter of the plaintext by different amounts.

The module includes three versions:
1. VigenereCipher - Initial incomplete implementation
2. VigenereCipherV2 - Complete working implementation
3. VigenereCipherV3 - Refactored version with DRY principle applied

How Vigenère Cipher Works:
    - Uses a keyword that repeats to match the plaintext length
    - Each letter is shifted based on the corresponding keyword letter
    - For encoding: shift forward by keyword letter position
    - For decoding: shift backward by keyword letter position

Example:
    Encrypt a message:

        >>> cipher = VigenereCipherV3("LEMON")
        >>> encrypted = cipher.encode("ATTACKATDAWN")
        >>> print(encrypted)
        'LXFOPVEFRNHR'
        >>> decrypted = cipher.decode(encrypted)
        >>> print(decrypted)
        'ATTACKATDAWN'

Attributes:
    ascii_uppercase (str): The uppercase ASCII alphabet from string module.

Note:
    This implementation only works with uppercase letters A-Z. Spaces and
    special characters are removed during encoding.
"""

from string import ascii_uppercase
from typing import Callable

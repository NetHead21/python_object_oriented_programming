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


def combine_chars(plain: str, key: str) -> str:
    """Encode a single plaintext character using a keyword character.

    Combines a plaintext character with a keyword character by shifting the
    plaintext forward in the alphabet by the position of the keyword character.
    This is the core encoding operation of the Vigenère cipher.

    Args:
        plain (str): A single character from the plaintext (A-Z, case-insensitive).
        key (str): A single character from the keyword (A-Z, case-insensitive).

    Returns:
        str: The encoded character (uppercase A-Z).

    Raises:
        ValueError: If either character is not in the alphabet.

    Example:
        >>> combine_chars('A', 'L')  # A(0) + L(11) = L(11)
        'L'
        >>> combine_chars('T', 'E')  # T(19) + E(4) = X(23)
        'X'
        >>> combine_chars('Z', 'B')  # Z(25) + B(1) = A(0) (wraps around)
        'A'

    Note:
        Uses modulo arithmetic to wrap around the alphabet (Z wraps to A).
    """

    plain = ascii_uppercase.index(plain.upper())
    key = ascii_uppercase.index(key.upper())
    return ascii_uppercase[(plain + key) % len(ascii_uppercase)]


def separate_chars(cipher: str, key: str) -> str:
    """Decode a single ciphertext character using a keyword character.

    Separates a ciphertext character from a keyword character by shifting the
    ciphertext backward in the alphabet by the position of the keyword character.
    This is the core decoding operation of the Vigenère cipher.

    Args:
        cipher (str): A single character from the ciphertext (A-Z, case-insensitive).
        key (str): A single character from the keyword (A-Z, case-insensitive).

    Returns:
        str: The decoded character (uppercase A-Z).

    Raises:
        ValueError: If either character is not in the alphabet.

    Example:
        >>> separate_chars('L', 'L')  # L(11) - L(11) = A(0)
        'A'
        >>> separate_chars('X', 'E')  # X(23) - E(4) = T(19)
        'T'
        >>> separate_chars('A', 'B')  # A(0) - B(1) = Z(25) (wraps around)
        'Z'

    Note:
        Uses modulo arithmetic to wrap around the alphabet (negative wraps to end).
        This is the inverse operation of combine_chars().
    """
    cipher = ascii_uppercase.index(cipher.upper())
    key = ascii_uppercase.index(key.upper())
    return ascii_uppercase[(cipher - key) % len(ascii_uppercase)]


class VigenereCipher:
    """Vigenère cipher implementation - Version 1 (Incomplete).

    This is an initial, incomplete implementation that demonstrates the basic
    structure of the cipher. The encode method returns a hardcoded value and
    there is no decode method.

    This version is included for educational purposes to show the evolution
    of the implementation. Use VigenereCipherV2 or VigenereCipherV3 for
    actual encryption/decryption.

    Attributes:
        keyword (str): The encryption keyword, stored in uppercase.

    Example:
        >>> cipher = VigenereCipher("LEMON")
        >>> # Note: This returns a hardcoded value, not actual encryption
        >>> cipher.encode("ATTACKATDAWN")
        'XECWQXUIVCRKHWA'

    Note:
        This is an incomplete implementation for demonstration purposes only.
        It does not perform actual encryption.
    """

    def __init__(self, keyword: str) -> None:
        """Initialize the cipher with a keyword.

        Args:
            keyword (str): The keyword to use for encryption (case-insensitive).
        """
        self.keyword = keyword.upper()

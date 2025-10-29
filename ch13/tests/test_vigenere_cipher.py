import sys
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.vigenere_cipher import (
    VigenereCipher,
    VigenereCipherV2,
    VigenereCipherV3,
    combine_chars,
    separate_chars,
)
import pytest


# Version 1. Incomplete


@pytest.fixture
def vigenere_train() -> VigenereCipher:
    cipher = VigenereCipher("TRAIN")
    return cipher


def test_encode(vigenere_train: VigenereCipher) -> None:
    encoded = vigenere_train.encode("ENCODEDINPYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


@pytest.mark.xfail(reason="Fails with version 1 of VigenereCipher - no decode method")
def test_decode(vigenere_train: VigenereCipher) -> None:
    decoded = vigenere_train.decode("XECWQXUIVCRKHWA")
    assert decoded == "ENCODEDINPYTHON"


@pytest.mark.xfail(reason="Fails with version 1 of VigenereCipher")
def test_encode_characters(vigenere_train: VigenereCipher) -> None:
    encoded = vigenere_train.encode("E")
    assert encoded == "X"


def test_encode_spaces(vigenere_train: VigenereCipher) -> None:
    encoded = vigenere_train.encode("encoded in Python")
    assert encoded == "XECWQXUIVCRKHWA"


def test_combine_character() -> None:
    assert combine_chars("E", "T") == "X"
    assert combine_chars("N", "R") == "E"


def test_extend_keyword(vigenere_train: VigenereCipher) -> None:
    extended = vigenere_train.extend_keyword(16)
    assert extended == "TRAINTRAINTRAINT"
    extend = vigenere_train.extend_keyword(5)
    assert extend == "TRAIN"


# Version 2. Complete


def test_separate_characters() -> None:
    assert separate_chars("X", "T") == "E"
    assert separate_chars("E", "R") == "N"


from string import ascii_uppercase


def test_combine_separate() -> None:
    for c in ascii_uppercase:
        for k in ascii_uppercase:
            assert separate_chars(combine_chars(c, k), k) == c


@pytest.fixture
def vigenere_v2_train() -> VigenereCipherV2:
    cipher = VigenereCipherV2("TRAIN")
    return cipher


def test_encode_v2(vigenere_v2_train: VigenereCipherV2) -> None:
    encoded = vigenere_v2_train.encode("ENCODEDINPYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


def test_decode_v2(vigenere_v2_train: VigenereCipherV2) -> None:
    decoded = vigenere_v2_train.decode("XECWQXUIVCRKHWA")
    assert decoded == "ENCODEDINPYTHON"


def test_encode_characters_v2(vigenere_v2_train: VigenereCipherV2) -> None:
    encoded = vigenere_v2_train.encode("E")
    assert encoded == "X"


@pytest.mark.xfail(reason="Fails with version 1 and 2 of VigenereCipher")
def test_encode_spaces_v2(vigenere_v2_train: VigenereCipherV2) -> None:
    encoded = vigenere_v2_train.encode("ENCODED IN PYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


@pytest.mark.xfail(reason="Fails with version 1 and 2 of VigenereCipher")
def test_encode_lowercase_v2(vigenere_v2_train: VigenereCipherV2) -> None:
    encoded = vigenere_v2_train.encode("encodedinpython")
    assert encoded == "XECWQXUIVCRKHWA"


# Version 3. Complete


@pytest.fixture
def vigenere_v3_train() -> VigenereCipherV3:
    cipher = VigenereCipherV3("TRAIN")
    return cipher


def test_encode_v3(vigenere_v3_train: VigenereCipherV3) -> None:
    encoded = vigenere_v3_train.encode("ENCODEDINPYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


def test_decode_v3(vigenere_v3_train: VigenereCipherV3) -> None:
    decoded = vigenere_v3_train.decode("XECWQXUIVCRKHWA")
    assert decoded == "ENCODEDINPYTHON"


def test_encode_characters_v3(vigenere_v3_train: VigenereCipherV3) -> None:
    encoded = vigenere_v3_train.encode("E")
    assert encoded == "X"


def test_encode_spaces_v3(vigenere_v3_train: VigenereCipherV3) -> None:
    encoded = vigenere_v3_train.encode("ENCODED IN PYTHON")
    assert encoded == "XECWQXUIVCRKHWA"


def test_encode_lowercase_v3(vigenere_v3_train: VigenereCipherV3) -> None:
    encoded = vigenere_v3_train.encode("encodedinpython")
    assert encoded == "XECWQXUIVCRKHWA"


def test_wraparound_behavior() -> None:
    # Z + B -> A, and A - B -> Z
    assert combine_chars("Z", "B") == "A"
    assert separate_chars("A", "B") == "Z"


def test_non_alpha_raises() -> None:
    # combine_chars/separate_chars should raise ValueError for non-alphabetic input
    import pytest

    with pytest.raises(ValueError):
        combine_chars("1", "A")

    with pytest.raises(ValueError):
        combine_chars("A", "!")

    with pytest.raises(ValueError):
        separate_chars("@", "A")


def test_empty_string_v2_and_v3(
    vigenere_v2_train: VigenereCipherV2, vigenere_v3_train: VigenereCipherV3
) -> None:
    # Encoding/decoding an empty string should return an empty string
    assert vigenere_v2_train.encode("") == ""
    assert vigenere_v2_train.decode("") == ""
    assert vigenere_v3_train.encode("") == ""
    assert vigenere_v3_train.decode("") == ""


def test_roundtrip_various_strings(
    vigenere_v2_train: VigenereCipherV2, vigenere_v3_train: VigenereCipherV3
) -> None:
    samples = ["A", "HELLO", "ATTACKATDAWN", "XYZ"]
    for s in samples:
        enc2 = vigenere_v2_train.encode(s)
        assert vigenere_v2_train.decode(enc2) == s.upper()

        enc3 = vigenere_v3_train.encode(s)
        assert vigenere_v3_train.decode(enc3) == s.upper()


def test_v3_handles_spaces_and_case() -> None:
    # V3 should remove spaces and work with mixed case
    cipher = VigenereCipherV3("LEMON")
    plaintext = "Attack At Dawn"
    ciphertext = cipher.encode(plaintext)
    assert ciphertext == "LXFOPVEFRNHR"
    assert cipher.decode(ciphertext) == "ATTACKATDAWN"


# Additional edge case tests


def test_single_character_keyword() -> None:
    """Test cipher with a single character keyword (Caesar cipher)"""
    cipher_v2 = VigenereCipherV2("A")
    cipher_v3 = VigenereCipherV3("A")

    # 'A' keyword means no shift (offset 0)
    assert cipher_v2.encode("HELLO") == "HELLO"
    assert cipher_v2.decode("HELLO") == "HELLO"

    assert cipher_v3.encode("HELLO") == "HELLO"
    assert cipher_v3.decode("HELLO") == "HELLO"


def test_keyword_longer_than_plaintext() -> None:
    """Test when keyword is longer than the plaintext"""
    cipher_v2 = VigenereCipherV2("VERYLONGKEYWORD")
    cipher_v3 = VigenereCipherV3("VERYLONGKEYWORD")

    plaintext = "HI"
    encoded_v2 = cipher_v2.encode(plaintext)
    encoded_v3 = cipher_v3.encode(plaintext)

    assert cipher_v2.decode(encoded_v2) == plaintext
    assert cipher_v3.decode(encoded_v3) == plaintext


def test_repeated_characters() -> None:
    """Test encoding of repeated characters"""
    cipher = VigenereCipherV3("KEY")

    # Same character repeated should encode differently based on keyword position
    encoded = cipher.encode("AAAA")
    # A + K, A + E, A + Y, A + K
    assert encoded == "KEYK"
    assert cipher.decode(encoded) == "AAAA"


def test_all_same_keyword_character() -> None:
    """Test with keyword containing all same characters"""
    cipher_v2 = VigenereCipherV2("BBB")
    cipher_v3 = VigenereCipherV3("BBB")

    plaintext = "HELLO"
    # Each character should shift by 1 (B offset)
    expected = "IFMMP"

    assert cipher_v2.encode(plaintext) == expected
    assert cipher_v3.encode(plaintext) == expected


def test_extend_keyword_edge_cases(vigenere_train: VigenereCipher) -> None:
    """Test extend_keyword with various edge cases"""
    # Extend to exact multiple of keyword length
    assert vigenere_train.extend_keyword(10) == "TRAINTRAIN"

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

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

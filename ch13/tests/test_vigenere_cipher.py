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

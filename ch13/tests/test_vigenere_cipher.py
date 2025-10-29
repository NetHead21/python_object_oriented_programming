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

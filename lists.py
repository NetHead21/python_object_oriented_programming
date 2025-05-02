import string

CHARACTERS = list(string.ascii_letters) + [" "]


def letter_frequency(sentence: str) -> list[tuple[str, int]]:
    frequencies = [(c, 0) for c in CHARACTERS]
    for letter in sentence:
        index = CHARACTERS.index(letter)
        frequencies[index] = (letter, frequencies[index][1] + 1)
    non_zero = [(letter, count) for letter, count in frequencies if count > 0]
    return non_zero


text = "A quick brown fox jumps over the lazy dog"
print(letter_frequency(text))

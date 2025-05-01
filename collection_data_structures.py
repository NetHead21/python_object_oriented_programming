stock = "AAPL", 123.52, 53.15, 137.98
stock2 = ("AAPL", 123.52, 53.15, 137.98)

print(f"{stock=}")
print(f"{stock2=}")
print(stock[2])
print(stock[1:3])

a = (42,)
b = (42,)
print(f"{a=}")
print(f"{b=}")

c = (
    (43, 3.14),
    (2.732, 3.224),
)
print(f"{c=}")


from typing import NamedTuple


# how to declare a namedtuple
class Stock(NamedTuple):
    symbol: str
    current: float
    high: float
    low: float


stock3 = Stock("AAPL", 243, 235, 53)

print(f"{stock3=}")
print(f"{stock3.symbol=}")
print(f"{stock3.current=}")
print(f"{stock3.high=}")

# tuple can have mutable elements
t = (1, [2, 3, 4])
print(f"{t=}")
t[1].append(5)
print(f"{t=}")


# namedtuple class with method
class Stock(NamedTuple):
    symbol: str
    current: float
    high: float
    low: float

    @property
    def middle(self) -> float:
        return (self.high + self.low) / 2


stock4 = Stock("MSFT", 123.23, 2323, 234)
print(f"{stock4=}")
print(f"{stock4.low=}")
print(f"{stock4.middle=}")


from dataclasses import dataclass


@dataclass
class Stock:
    symbol: str
    current: float
    high: float
    low: float


stock5 = Stock("MSFT", 123.23, 2323, 234)
print(f"{stock5}")
print(f"{stock5.current=}")
stock5.unexpected_attribute = "allowed"
print(f"{stock5}")


@dataclass(order=True)
class StockOrdered:
    name: str
    current: float = 0.0
    high: float = 0.0
    low: float = 0.0


stock_ordered1 = StockOrdered("GOOG", 1826.77, 1847.20, 1013.54)
stock_ordered2 = StockOrdered("GOOG")
stock_ordered3 = StockOrdered("GOOG", 1728.28, high=1733.18, low=1666.33)

print(f"{stock_ordered1}")
print(f"{stock_ordered2}")
print(f"{stock_ordered3}")

print(stock_ordered1 < stock_ordered2)
print(stock_ordered1 > stock_ordered2)


# using python dictionary
def letter_frequency(sentence: str) -> dict[str, int]:
    frequencies: dict[str, int] = {}
    for letter in sentence:
        frequency = frequencies.setdefault(letter, 0)
        frequencies[letter] = frequency + 1
    return frequencies


from collections import defaultdict


def letter_frequency_2(sentence: str) -> defaultdict[str, int]:
    frequencies: defaultdict[str, int] = defaultdict(int)
    for letter in sentence:
        frequencies[letter] += 1
    return frequencies


print(letter_frequency("hello world"))
print(letter_frequency_2("hello world"))


def word_count(words: list) -> dict[str, int]:
    word_counts: defaultdict[str, int] = defaultdict(int)
    for word in words:
        word_counts[word] += 1

    return word_counts


words = ["apple", "banana", "apple", "orange", "banana", "apple"]
print(word_count(words))


@dataclass
class Prices:
    current: float = 0.0
    high: float = 0.0
    low: float = 0.0


portfolio = defaultdict(Prices)
print(portfolio["GOOG"])
portfolio["AAPL"] = Prices(current=122.25, high=137.98, low=53.15)

from pprint import pprint
from collections import Counter

pprint(portfolio)


def letter_frequency_3(sentence: str) -> Counter[str]:
    return Counter(sentence)


responses = [
    "vanilla",
    "chocolate",
    "vanilla",
    "vanilla",
    "caramel",
    "strawberry",
    "vanilla",
]

favorites = Counter(responses).most_common(1)
name, frequency = favorites[0]
print(f"{name=}")
print(f"{frequency=}")

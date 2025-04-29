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

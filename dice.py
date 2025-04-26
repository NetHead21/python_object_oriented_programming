import random
import abc
from typing import cast, Type, Iterable, Any, Optional


class Die(abc.ABC):
    def __init__(self) -> None:
        self.face: int
        self.roll()

    @abc.abstractmethod
    def roll(self) -> None: ...

    def __repr__(self) -> str:
        return f"{self.face}"

    def __mul__(self, other: Any) -> "DDice":
        if isinstance(other, int):
            return DDice(type(self)) * other
        return NotImplemented

    def __rmul__(self, other: Any) -> "DDice":
        if isinstance(other, int):
            return other * DDice(type(self))
        return NotImplemented


class D4(Die):
    def roll(self) -> None:
        self.face = random.choice((1, 2, 3, 4))


class D6(Die):
    def roll(self) -> None:
        self.face = random.randint(1, 6)


class D8(Die):
    def roll(self) -> None:
        self.face = int(random.random() * 8)


class Dice(abc.ABC):
    def __init__(self, n: int, die_class: Type[Die]) -> None:
        self.dice = [die_class() for _ in range(n)]

    @abc.abstractmethod
    def roll(self) -> None: ...

    @property
    def total(self) -> int:
        return sum(d.face for d in self.dice)


class SimpleDice(Dice):
    def roll(self) -> None:
        for d in self.dice:
            d.roll()


class YachtDice(Dice):
    def __init__(self) -> None:
        super().__init__(5, D6)
        self.save: set[int] = set()

    def saving(self, positions: Iterable[int]) -> "YachtDice":
        if not all(0 <= n < 6 for n in positions):
            raise ValueError("Invalid position")
        self.saved = set(positions)
        return self

    def roll(self) -> None:
        for n, d in enumerate(self.dice):
            if n not in self.saved:
                d.roll()
        salf.saved = set()


if __name__ == "__main__":
    random.seed(42)
    dice = [D4(), D4(), D4()]
    faces = [d.face for d in dice]
    print(faces)

from typing import Optional, Type, Literal
from types import TracebackType


class StringJoiner(list[str]):
    def __enter__(self) -> "StringJoiner":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        self.result = "".join(self)
        return False


with StringJoiner("Hello") as sj:
    sj.append(", ")
    sj.append("world")
    sj.append("!")

print(sj.result)

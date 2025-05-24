from typing import Optional, Type, Literal
from types import TracebackType

class StirngJoiner(list[str]):
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

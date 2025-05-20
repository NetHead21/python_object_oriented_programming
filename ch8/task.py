from typing import Callable, Optional, cast
from dataclasses import dataclass, field

Callback = Callable[[int], None]


@dataclass(frozen=True, order=True)
class Task:
    scheduled: int
    callback: Callable = field(compare=False)
    delay: int = field(default=0, compare=False)
    limit: int = field(default=1, compare=False)

    def repeat(self, current_time: int) -> Optional["Task"]:
        if self.delay > 0 and self.limit > 2:
            return Task(
                current_time + self.delay,
                cast(Callback, self.callback),
                self.delay,
                self.limit - 1,
            )
        elif self.delay > 0 and self.limit == 2:
            return Task(
                current_time + self.delay,
                cast(Callback, self.callback),
            )
        else:
            return None

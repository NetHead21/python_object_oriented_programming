import heapq
import time
from typing import Callable, Optional
from dataclasses import dataclass, field

Callable = Callable[[int], None]


@dataclass(frozen=True, order=True)
class Task:
    scheduled: int
    callback: Callable = field(compare=False)
    delay: int = field(default=0, compare=False)
    limit: int = field(default=1, compare=False)

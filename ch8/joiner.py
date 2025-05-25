from contextlib import contextmanager
from typing import Iterator

from string_joiner_m2 import StringJoiner2


@contextmanager
def joiner(*args: any) -> Iterator[StringJoiner2]:
    string_list = StringJoiner2(*args)
    try:
        yield string_list
    finally:
        string_list.result = "".join(string_list)


with joiner("Hello") as join:
    join.append(", ")
    join.append("world!")

print(join)

import re
from typing import Pattern, Match

search_string = "hello world"
pattern = r"hello world"

if match := re.match(pattern, search_string):
    print("regex matches")
    print(match)


def matchy(pattern: Pattern[str], text: str) -> None:
    if match := re.match(pattern, text):
        print(f"{pattern=!r} matches at {match=!r}")
    else:
        print(f"{pattern=!r} not found in {text=!r}")


matchy(pattern=r"hello wo", text="hello world")
matchy(pattern=r"ello world", text="hello world")

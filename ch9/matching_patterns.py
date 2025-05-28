import re
from typing import Pattern, Match, Optional

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


def email_domain(text: str) -> Optional[str]:
    email_pattern = f"[a-z0-9._%+-]+@([a-z0-9.-]+\.[a-z]{2,})"
    if match := re.match(email_pattern, text, re.IGNORECASE):
        return match.group(1)
    else:
        return None


def email_domain_2(text: str) -> Optional[str]:
    email_pattern = r"(?P<name>[a-z0-9._%+-]+)@(?P<domain>[a-z0-9.-]+\.[a-z]{2,})"
    if match := re.match(email_pattern, text, re.IGNORECASE):
        return match.groupdict()["domain"]
    else:
        return None

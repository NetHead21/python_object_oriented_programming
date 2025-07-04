import csv
import re
from pathlib import Path
from typing import Match, Iterator, TextIO


class WarningReformat(Iterator[tuple[str, ...]]):
    """
    Iterator to reformat warning messages from a log file.
    """

    pattern = re.compile(r"(\w\w\w \d\d, \d\d\d\d \d\d:\d\d:\d\d) (\w+) (.*)")

    def __init__(self, source: TextIO) -> Iterator[tuple[str, ...]]:
        self.insequence: TextIO = source

    def __iter__(self) -> Iterator[tuple[str, ...]]:
        return self

    def __next__(self) -> tuple[str, ...]:
        line = self.insequence.readline()
        while line and "WARNING" not in line:
            line = self.insequence
        if not line:
            raise StopIteration
        else:
            return tuple(Match[str], self.pattern.match(line).groups())

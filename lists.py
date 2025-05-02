import string

CHARACTERS = list(string.ascii_letters) + [" "]


def letter_frequency(sentence: str) -> list[tuple[str, int]]:
    frequencies = [(c, 0) for c in CHARACTERS]
    for letter in sentence:
        index = CHARACTERS.index(letter)
        frequencies[index] = (letter, frequencies[index][1] + 1)
    non_zero = [(letter, count) for letter, count in frequencies if count > 0]
    return non_zero


text = "A quick brown fox jumps over the lazy dog"
print(letter_frequency(text))


from typing import Optional, cast, Any
from dataclasses import dataclass
import datetime
from datetime import timezone


@dataclass(frozen=True)
class MultiItem:
    data_source: str
    timestamp: Optional[float]
    creation_date: Optional[str]
    name: str
    owner_etc: str

    def __lt__(self, other: Any) -> bool:
        if self.data_source == "Local":
            self_datetime = datetime.datetime.fromtimestamp(
                cast(float, self.timestamp), tz=timezone.utc
            )
        else:
            self_datetime = datetime.datetime.fromisoformat(
                cast(str, self.creation_date)
            ).replace(tzinfo=timezone.utc)
        if other.data_source == "Local":
            other_datetime = datetime.datetime.fromtimestamp(
                cast(float, other.timestamp), tz=timezone.utc
            )
        else:
            other_datetime = datetime.datetime.fromisoformat(
                cast(str, other.creation_date)
            ).replace(tzinfo=timezone.utc)
        return self_datetime < other_datetime

    def __eq__(self, other: object) -> bool:
        return self.datetime == cast(MultiItem, other).datetime

    @property
    def datetime(self) -> datetime.datetime:
        if self.data_source == "Local":
            return datetime.datetime.fromtimestamp(
                cast(float, self.timestamp), tz=timezone.utc
            )
        else:
            return datetime.datetime.fromisoformat(
                cast(str, self.creation_date)
            ).replace(tzinfo=timezone.utc)


mi_0 = MultiItem("Local", 1607262522.000000, None, "Some File", "etc. 0")
mi_1 = MultiItem("Remote", None, "2020-12-06T13:47:52.000001", "Another File", "etc. 1")
mi_2 = MultiItem("Local", 1579355292.000002, None, "This File", "etc. 2")
mi_3 = MultiItem("Remote", None, "2020-01-18T13:48:12.000003", "That File", "etc. 3")
file_list = [mi_0, mi_1, mi_2, mi_3]
file_list.sort()
print([f.datetime for f in file_list])

from pprint import pprint

pprint(file_list)

from functools import total_ordering


@total_ordering
class MultiItemTO(MultiItem): ...

from .format_time import format_time
from .task import Task
from .repeater import Repeater


def one(timer: float) -> None:
    format_time("Called One")


def two(timer: float) -> None:
    format_time("Called Two")


def three(timer: float) -> None:
    format_time("Called Three")




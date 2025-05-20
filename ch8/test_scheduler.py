from format_time import format_time
from task import Task
from repeater import Repeater
from scheduler import Scheduler


def one(timer: float) -> None:
    format_time("Called One")


def two(timer: float) -> None:
    format_time("Called Two")


def three(timer: float) -> None:
    format_time("Called Three")


s = Scheduler()
s.enter(1, one)
s.enter(2, one)
s.enter(2, two)
s.enter(4, two)
s.enter(3, three)
s.enter(6, three)
repeater = Repeater()
s.enter(5, repeater.four, delay=1, limit=5)
s.run()

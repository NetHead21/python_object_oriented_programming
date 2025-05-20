import heapq
import time

from .task import Callback, Task


class Scheduler:
    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def enter(
        self,
        after: int,
        task: Callback,
        delay: int = 0,
        limit: int = 1,
    ) -> None:
        new_task = Task(after, task, delay, limit)
        heapq.heappush(self.task, new_task)

    def run(self) -> None:
        current_time = 0
        while self.tasks:
            next_task = heapq.heappop(self.tasks)
            if (delay := next_task.scheduled - current_time) > 0:
                time.sleep(next_task.scheduled - current_time)
            current_time = next_task.scheduled
            next_task.callback(current_time)
            if again := next_task.repeat(current_time):
                heapq.heappush(self.tasks, again)

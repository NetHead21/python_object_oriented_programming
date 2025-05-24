from format_time import format_time

class Repeater_2:
    def __init__(self) -> None:
        self.count = 0

    def __call__(self, timer: float) -> None:
        self.count += 1
        format_time(f"Called Four: {self.count}")


rpt = Repeater_2()
rpt(1)
rpt(2)
rpt(3)
rpt(4)

from format_time import format_time

class Repeater_2:
    def __init__(self) -> None:
        self.count = 0

    def __call__(self, timer: float) -> None:
        self.count += 1
        format_time(f"Called Four: {self.count}")


rpt = Repeater_2()
print(rpt(1))
print(rpt(2))
print(rpt(3))
print(rpt(4))

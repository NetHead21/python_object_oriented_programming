class Repeater_2:
    def __init__(self) -> None:
        self.count = 0

    def __call__(self, timer: float) -> none:
        self.count += 1
        format_time(f"Called Four: {self.count}")

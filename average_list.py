class AverageList(list[int]):
    @property
    def average(self) -> float:
        return sum(self) / len(self)


if __name__ == "__main__":
    a = AverageList([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5])
    print(a.average)

class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius  # Getter method

    @radius.setter
    def radius(self, value: float | int) -> None:
        if value <= 0:
            raise ValueError("Radius must be positive.")
        self._radius = value  # Setter method

    @property
    def area(self):
        # Computer value; no setter as this is derived from radius
        return 3.14159 * self._radius**2


if __name__ == "__main__":
    circle = Circle(5)
    print(circle.radius)  # Access radius
    circle.radius = 10  # Set radius
    print(circle.area)  # Compute area based on radius

from math import hypot
from typing import Optional, Iterable


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def distance(self, other: "Point") -> float:
        return hypot(self.x - other.x, self.y - other.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


Pair = tuple[float, float]
Point_or_Tuple = Point | Pair


class BasePolygon:
    def perimeter(self) -> float:
        pairs = zip(self.vertices, self.vertices[1:] + self.vertices[:1])
        return sum(p1.distance(p2) for p1, p2 in pairs)


class Polygon(BasePolygon):
    def __init__(self) -> None:
        self.vertices: list[Point] = []

    def add_point(self, point: Point) -> None:
        self.vertices.append((point))


class Polygon_2(BasePolygon):
    def __init__(self, vertices: Optional[Iterable[Point]] = None) -> None:
        self.vertices = list(vertices) if vertices else []


class Polygon_3(BasePolygon):
    def __init__(self, vertices: Optional[Iterable[Point_or_Tuple]] = None) -> None:
        self.vertices: list[Point] = []
        if vertices:
            for point_or_tuple in vertices:
                self.vertices.append(self.make_point(point_or_tuple))

    @staticmethod
    def make_point(item: Point_or_Tuple) -> Point:
        return item if isinstance(item, Point) else Point(*item)


if __name__ == "__main__":
    square = Polygon()
    s_point_1 = Point(1, 1)
    s_point_2 = Point(1, 2)
    s_point_3 = Point(2, 2)
    s_point_4 = Point(2, 1)
    square.add_point(s_point_1)
    square.add_point(s_point_2)
    square.add_point(s_point_3)
    square.add_point(s_point_4)
    print(f"The perimeter of square is {square.perimeter()}")

    t_point_1 = Point(-1, 6)
    t_point_2 = Point(3, -3)
    t_point_3 = Point(-4, -1)

    print(
        f"The distance between point {t_point_1} and point {t_point_2} is {t_point_1.distance(t_point_2)}"
    )
    print(
        f"The distance between point {t_point_2} and point {t_point_3} is {t_point_2.distance(t_point_3)}"
    )
    print(
        f"The distance between point {t_point_3} and point {t_point_1} is {t_point_3.distance(t_point_1)}"
    )
    triangle_1 = Polygon_2([t_point_1, t_point_2, t_point_3])
    print(f"The perimeter of traiangle_1 is {triangle_1.perimeter()}")

    r_point_1 = Point(-6, -4)
    r_point_2 = Point(-2, 0)
    r_point_3 = Point(0, -2)
    r_point_4 = Point(-4, -6)
    rectangle = Polygon_3((r_point_1, r_point_2, r_point_3, r_point_4))
    print(f"The perimeter of the rectangle is {rectangle.perimeter()}")

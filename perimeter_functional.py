from math import hypot

Point = tuple[float, float]
Polygon = list[Point]


def distance(p_1: Point, p_2: Point) -> float:
    """This function will return the distance
    between two points"""
    return hypot(p_1[0] - p_2[0], p_1[1] - p_2[1])


def perimeter(polygon: Polygon) -> float:
    """This function will return the perimeter
    of a polygon"""
    pairs = zip(polygon, polygon[1:] + polygon[:1])
    return sum(distance(p1, p2) for p1, p2 in pairs)


if __name__ == "__main__":
    point_1 = Point((-3, -1))
    point_2 = Point((2, 3))
    point_3 = Point((2, -1))

    print(
        f"The distance between {point_1} to {point_2} is {distance(point_1, point_2)}"
    )
    print(
        f"The distance between {point_2} to {point_3} is {distance(point_2, point_3)}"
    )
    print(
        f"The distance between {point_3} to {point_1} is {distance(point_3, point_1)}"
    )
    triangle_1 = Polygon([point_1, point_2, point_3])
    print(f"The perimeter of trangle_1 is {perimeter(triangle_1)}")

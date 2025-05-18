# function with no parameters
def no_params() -> str:
    return "Hello, world!"


print(no_params())


# function with parameters
def mandatory_params(x: any, y: any, z: any) -> str:
    return f"{x=}, {y=}, {z=}"


a_variable = 42
print(mandatory_params("a string", a_variable, True))


# function with default values for parameters
from typing import Optional


def latitude_dms(
    deg: float, min: float, sec: float = 0.0, dir: Optional[str] = None
) -> str:
    if dir is None:
        dir = "N"
    return f"{deg:02.0f} {min + sec / 60:05.3f}{dir}"


print(latitude_dms(36, 51, 2.9, "N"))
print(latitude_dms(38, 58, dir="N"))


# keywords only functions
def kw_only(x: any, y: str = "defaultkw", *, a: bool, b: str = "only") -> str:
    return f"{x=}, {y=}, {a=}, {b=}"


print(kw_only("x", a="a", b="b"))
# print(kw_only("x")) # will generate error
# print(kw_only("x", "y", "a")) # will generate error


# positional-only parameters function
def pos_only(x: any, y: str, /, z: Optional[any] = None) -> str:
    return f"{x=}, {y=}, {z=}"


print(pos_only(2, "three"))
print(pos_only(2, "three", 3.14159))
# print(pos_only(x=2, y="three")) # will generate error


# Additional details on defaults
# Default arguments is evaluated once when the function
# is first created, not when it is evaluated.
def add_item(item: str, items: list[str] = []) -> list:
    items.append(item)
    return items


print(add_item("apple"))  # Output ['apple']
print(add_item("banana"))  # Output ['apple', 'banana']

# the same list items is being modified across multiple
# funciton calls. Instead of getting a new list each
# time, the previous item remain.


# the correct approach
def add_item(item: str, items: list[str] = None) -> list:
    if items is None:
        items = []
    items.append(item)
    return items


print(add_item("apple"))  # Output ['apple']
print(add_item("banana"))  # Output ['apple']


number = 5


def funky_function(x: int = number) -> str:
    return f"{x=}, {number=}"


print(funky_function(42))

number = 5

print(funky_function())


def better_function(x: Optional[int] = None) -> str:
    if x is None:
        x = number
    return f"better: {x=}, {number=}"


def better_function_2(x: Optional[int] = None) -> str:
    x = number if x is None else x
    return f"better: {x=}, {number=}"

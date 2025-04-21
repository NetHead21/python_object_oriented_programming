from typing import NoReturn


def never_returns() -> NoReturn:
    print("I am about to raise an exeption")
    raise Exception("This is always raised")
    print("This line will never execute")
    return "I won't be returned"

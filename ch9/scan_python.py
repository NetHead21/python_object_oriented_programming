from pathlib import Path
from typing import Callable


def scan_python_1(path: Path) -> int:
    sloc = 0
    with path.open() as source:
        for line in source:
            line = line.strip()
            if line and not line.startswith("#"):
                sloc += 1
    return sloc


def count_sloc(path: Path, scanner: Callable[[Path], int]) -> int:
    if path.name.startswith("."):
        return 0
    elif path.is_file():
        if path.suffix != ".py":
            return 0
        with path.open() as source:
            return scanner(path)
    elif path.is_dir():
        count = sum(count_sloc(name, scanner) for name in path.iterdir())
        return count
    else:
        return 0


base = Path.cwd().parent
chapter = base / "ch9"

count = count_sloc(chapter, scan_python_1)
print(f"{chapter.relative_to(base)}: {count} lines of code")

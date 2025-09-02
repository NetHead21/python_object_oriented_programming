import abc
import argparse
import contextlib
from pathlib import Path
import sys
from typing import Optional


class Node(abc.ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self.parent: Optional["Folder"] = None

    def move(self, new_place: "Folder") -> None:
        previous = self.parent
        new_place.add_child(self)
        if previous:
            del previous.children[self.name]

    @abc.abstractmethod
    def copy(self, new_folder: "Folder") -> None: ...

    @abc.abstractmethod
    def remove(self) -> None: ...

    @abc.abstractmethod
    def tree(
        self, indent: int = 0, last: bool = False, outer: bool = False
    ) -> None: ...

    @abc.abstractmethod
    def dot(self) -> None: ...


class Folder(Node):
    def __init__(self, name: str, children: Optional[dict[str, "Node"]] = None) -> None:
        super().__init__(name)
        self.children = children or {}

    def __repr__(self) -> str:
        return f"Folder({self.name!r}, {self.children!r})"

    def add_child(self, node: "Node") -> "Node":
        node.parent = self
        self.children[node.name] = node
        return node

    def copy(self, new_folder: "Folder") -> None:
        target = new_folder.add_child(Folder(self.name))
        for c in self.children:
            self.children[c].copy(target)

    def remove(self) -> None:
        names = list(self.children)
        for c in names:
            self.children[c].remove()

        if self.parent:
            del self.parent.children[self.name]

    def tree(self, indent: int = 0, last: bool = False, outer: bool = False) -> None:
        indent_text = "     " if outer else " |   "
        print((indent * indent_text) + " +--", self.name)
        if self.children:
            *first, final = list(self.children)
            for c in first:
                self.children[c].tree(indent + 1, last=False, outer=outer)
            self.children[final].tree(indent + 1, last=True, outer=outer)

    def dot(self) -> None:
        for c in self.children:
            print(f"    n{id(self)} -> n{id(self.children[c])};")
            self.children[c].dot()
        print(f'    n{id(self)} [label = "{self.name}"];')


class File(Node):
    def __repr__(self) -> str:
        return f"File({self.name!r})"

    def copy(self, new_folder: "Folder") -> None:
        new_folder.add_child(File(self.name))

    def remove(self) -> None:
        if self.parent:
            del self.parent.children[self.name]

    def tree(self, indent: int = 0, last: bool = False, outer: bool = False) -> None:
        indent_text = "     " if outer else " |   "
        print((indent * indent_text) + " +--", self.name)

    def dot(self) -> None:
        print(f'    n{id(self)} [shape=box,label="{self.name}"];')


f = File("name.ex")
print(f.tree())

d = Folder("Folder")
d.add_child(f)
print(d.tree())

d_p = Folder("Parent", {"Folder": d})
print(d_p.tree())


def dump(tree: Folder) -> None:
    """Top-level dump with special 'outer' rule."""
    print("tree.name")
    *first, final = list(tree.children)
    for c in first:
        tree.children[c].tree(outer=False)
    tree.children[final].tree(outer=True)


def dot(tree: Folder) -> None:
    print("digraph tree {")
    print("    rankdir=LR;")
    print("    ratio=auto;")
    print("    nodesep=.125;")
    tree.dot()
    print("}")


def populate(base: Path) -> Folder:
    tree = Folder(base.name)
    for item in base.glob("**/*"):
        if any(n.startswith(".") for n in item.parts):
            # Ignore directories like ".tox"
            continue
        if any(n.startswith("__") and n.endswith("__") for n in item.parts):
            # Ignore directories like "__pycache__"
            continue
        if item.is_file():
            here = tree
            for parent_name in item.relative_to(base).parts[:-1]:
                here = here.add_child(Folder(parent_name))
            here.add_child(File(item.name))
    return tree


def main(argv: list[str] = sys.argv[1:]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs=1, type=Path)
    options = parser.parse_args(argv)

    tree = populate(options.directory[0])
    dump(tree)

    with Path("tree.dot").open("w") as target:
        with contextlib.redirect_stdout(target):
            dot(tree)


if __name__ == "__main__":
    main()

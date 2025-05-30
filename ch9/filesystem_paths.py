import os.path
from pathlib import Path


path = os.path.abspath(
    os.sep.join(["", "Users", "Admin", "subdir", "subsubdir", "file.txt"])
)
print(path)


path = Path("/Users") / "Admin" / "subdir" / "subsubdir" / "file.txt"
print(path)

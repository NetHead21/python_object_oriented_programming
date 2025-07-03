from pathlib import Path
from pprint import pprint


def analyze_directory_sizes(directory_path: Path):
    """Analyze file sizes in a directory."""
    if not directory_path.exists():
        return {}

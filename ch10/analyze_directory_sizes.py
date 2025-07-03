from pathlib import Path
from pprint import pprint


def analyze_directory_sizes(directory_path: Path):
    """Analyze file sizes in a directory."""
    if not directory_path.exists():
        return {}

    files = [f for f in directory_path.iterdir() if f.is_file()]

    if not files:
        return {"error": "No files found"}

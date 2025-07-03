from pathlib import Path
from pprint import pprint


def analyze_directory_sizes(directory_path: Path):
    """Analyze file sizes in a directory."""
    if not directory_path.exists():
        return {}

    files = [f for f in directory_path.iterdir() if f.is_file()]

    if not files:
        return {"error": "No files found"}

    return {
        "total_size": sum(f.stat().st_size for f in files),
        "largest_file_size": max(f.stat().st_size for f in files),
        "smallest_file_size": min(f.stat().st_size for f in files),
        "avg_file_size": sum(f.stat().st_size for f in files) / len(files),
        "python_files_size": sum(f.stat().st_size for f in files if f.suffix == ".py"),
        "log_files_count": sum(1 for f in files if f.suffix == ".log"),
    }


def main():
    SCRIPT_DIR = Path(__file__).parent
    pprint(analyze_directory_sizes(SCRIPT_DIR))


if __name__ == "__main__":
    main()

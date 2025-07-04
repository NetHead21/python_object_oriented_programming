import csv
import re
from pathlib import Path
from typing import Iterator, TextIO


class WarningReformat(Iterator[tuple[str, ...]]):
    """
    Iterator to reformat warning messages from a log file.
    """

    # Fixed pattern to handle single-digit days
    pattern = re.compile(r"(\w{3} \d{1,2}, \d{4} \d{2}:\d{2}:\d{2}) (\w+) (.*)")

    def __init__(self, source: TextIO) -> None:  # Fixed return type
        self.insequence: TextIO = source

    def __iter__(self) -> Iterator[tuple[str, ...]]:
        return self

    def __next__(self) -> tuple[str, ...]:
        line = self.insequence.readline()
        # Fixed: Continue reading until we find a WARNING line or reach end
        while line and "WARNING" not in line:
            line = self.insequence.readline()  # Fixed: was missing .readline()

        if not line:
            raise StopIteration

        # Fixed: Proper regex matching and tuple creation
        match = self.pattern.match(line.strip())
        if match:
            return match.groups()
        else:
            # If line doesn't match pattern, try next line
            return self.__next__()


def extract_and_parse_2(full_log_path: Path, warning_log_path: Path) -> None:
    """Extract and parse warning messages from log file."""
    with warning_log_path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target, delimiter="\t")
        # Write header
        writer.writerow(["timestamp", "level", "message"])

        with full_log_path.open(encoding="utf-8") as source:  # Added encoding
            filter_reformat = WarningReformat(source)
            for line_groups in filter_reformat:
                writer.writerow(line_groups)


def main() -> None:
    full_log_path = Path.cwd() / "data" / "sample.log"
    warning_log_path = Path.cwd() / "data" / "warning.log"

    if not full_log_path.exists():
        raise FileNotFoundError(f"Log file not found: {full_log_path}")

    print("Processing log file...")
    extract_and_parse_2(full_log_path, warning_log_path)
    print(f"Warning messages extracted to: {warning_log_path}")

    # Fixed: Better way to display results
    if warning_log_path.exists():
        with warning_log_path.open(encoding="utf-8") as f:
            lines = f.readlines()
            print(f"Found {len(lines)-1} warning messages:")  # -1 for header
            for line in lines[:5]:  # Show first 5 lines
                print(f"  {line.strip()}")
            if len(lines) > 5:
                print(f"  ... and {len(lines)-5} more")


if __name__ == "__main__":
    main()

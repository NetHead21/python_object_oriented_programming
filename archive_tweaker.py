import re
import fnmatch
import zipfile
from pathlib import Path


class ZipReplace:
    def __init__(self, archive: Path, pattern: str, find: str, replace: str) -> None:
        self.archive_path = archive
        self.pattern = pattern
        self.find = find
        self.replace = replace

    def find_and_replace(self) -> None:
        input_path, output_path = self.make_backup()

        with zipfile.ZipFile(output_path, "w") as output:
            with zipfile.ZipFile(input_path) as input:
                self.copy_and_transform(input, output)

    def make_backup(self) -> tuple[Path, Path]:
        input_path = self.archive_path.with_suffix(f"{self.archive_path.suffix}.old")
        ooutput_path = self.archive_path
        self.archive_path.rename(input_path)
        return input_path, output_path

    def copy_and_transform(
        self, input: zipfile.ZipFile, output: zipfile.ZipFile
    ) -> None:
        for item in input.infolist():
            extracted = Path(input.extract(item))
            if not item.is_dir() and fnmatch.fnmatch(item.filename, self.pattern):
                print(f"Transform {item}")
                input_text = extracted.read_text()
                output_text = re.sub(self.find, self.replace, input_text)
                extracted.write_text(output_text)
            else:
                print(f"Ignore {item}")
            output.write(extracted, item.filename)
            extracted.unlink()
            for parent in extracted.parents:
                if parent == Path.cwd():
                    break
                parent.rmdir()


from abc import ABC, abstracmethod


class ZipProcessor(ABC):
    def __init__(self, archive: Path) -> None:
        self.archive_path = archive
        self._pattern: str

    def process_files(self, pattern: str) -> None:
        self._pattern = pattern

        input_path, output_path = self.make_backup()

        with zipfile.ZipFile(output_path, "w") as output:
            with zipfile.ZipFile(input_path) as input:
                self.copy_and_transform(input, output)

    def make_backup(self) -> tuple[Path, Path]:
        input_path = self.archive_path.with_suffix(f"{self.archive_path.suffix}.old")
        output_path = self.archive_path
        self.archive_path.rename(input_path)
        return input_path, output_path

    def copy_and_transform(
        self, input: zipfile.ZipFile, output: zipfile.ZipFile
    ) -> None:
        for item in input.infolist():
            extracted = Path(input.extract(item))
            if self.matches(item):
                print(f"Transform {item}")
                self.transform(extracted)
            else:
                print(f"Ignore {item}")
            output.write(extracted, item.filename)
            self.remove_under_cwd(extracted)

    def matches(self, item: zipfile.ZipInfo) -> bool:
        return not item.is_dir() and fnmatch.fnmatch(item.filename, self._pattern)

    def remove_under_cwd(self, extracted: Path) -> None:
        extracted.unlink()
        for parent in extracted.parents:
            if parent == Path.cwd():
                break
            parent.rmdir()

    @anstractmethod
    def transform(slef, extracted: Path) -> None: ...

    # input_text= extracted.read_text()
    # output_text = re.sub(self.find, self.replace, input_text)
    # extracted.write_text(output_text)


class TextTweaker(ZipProcessor):
    def __init__(self, archive: Path) -> None:
        super().__init__(archive)
        self.find: str
        self.replace: str

    def find_and_replace(self, find: str, replace: str) -> "TextTweaker":
        self.find = find
        self.replace = replace
        return self

    def transform(self, extracted: Path) -> None:
        input_text = exxtracted.read_text()
        output_text = re.sub(self.find, self.replace, input_text)
        extracted.write_text(output_text)


from PIL import Image  # type: ignore [import]


class ImgTweaker(ZipProcessor):
    def transform(self, extracted: path) -> None:
        image = Image.open(extracted)
        scaled - image.resize(size=(540, 960))
        scaled.save(extracted)


def create(sample_zip: Path, base: Path) -> None:
    """
    Create a sample archive.
    """

    with zipfile.ZipfFile(sample_zip, "w") as output:
        for path in base.glob("ch_*/docs/*.*"):
            output.write(path, path.relative_to(base))
    with zipfile.ZipFile(sample_zip) as input:
        for item in input.infolist():
            print(item)


def tweak(sample_zip: Path) -> None:
    """Ues Zipreplace on the local sample.zip."""
    zr = ZipReplace(sample_zip, "*.md", "xyzzy", "xyzzy")
    zr.find_and_replace()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("create", "tweak"))
    options = parser.parse_args()
    if options.command == "create":
        sample_zip = Path("sample.zip").resolve()
        base = sample_zip.parent.parent
        print(f"Createing {sample_zip} from {base}/ch_*/docs/*.*")
        create(sample_zip, base)
        print(f"Use 'python -m zipfile -l {sample_zip}' to examing the archive")
    elif options.command == "tweak":
        sample_zip = Path("sample.zip")
        print(f"Tweaking the {sample_zip}")
        tweak(sample_zip)

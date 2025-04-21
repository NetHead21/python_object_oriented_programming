import time
from urllib.request import urlopen
from typing import Optional, cast


class WebPage:
    def __init__(self, url: str) -> None:
        self.url = url
        self._content: Optional[bytes] = None

    @property
    def content(self) -> bytes:
        if self._content is None:
            print("Retrieving New Page...")
            with urlopen(self.url) as response:
                self._content = response.read()
        return self._content


if __name__ == "__main__":
    webpage = WebPage("http://ccphillips.net/")

    now = time.perf_counter()
    content1 = webpage.content
    print(content1)

    first_fetch = time.perf_counter() - now

    now = time.perf_counter()
    content2 = webpage.content
    second_fetch = time.perf_counter() - now

    assert content2 == content1, "Problem: Pages were different"
    print(f"Initial Request {first_fetch:5f}")
    print(f"Subsequent Requests {second_fetch:.5f}")

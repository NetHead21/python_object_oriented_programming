from urllib.parse import urlparse
from pathlib import Path


def get_pages(*links: str) -> None:
    for link in links:
        url = urlparse(link)
        name = "index.html" if url.path in ("", "/") else url.path
        target = Path(url.netloc.replace(".", "_")) / name
        print(f"Create {target} from {link}")


get_pages()
get_pages("https://www.archlinux.org")
get_pages(
    "https://www.archlinux.org",
    "https://dusty.phillips.codes",
    "https://itmaybeahack.com",
)

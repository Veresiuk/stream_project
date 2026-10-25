import csv
from collections.abc import Iterable, Iterator

def parse_csv_rows(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    """Розбір рядків у словники за допомогою csv.DictReader."""
    reader = csv.DictReader(lines)
    yield from reader
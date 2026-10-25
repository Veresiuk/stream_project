from collections.abc import Iterator
from pathlib import Path

def stream_read_lines(path: Path) -> Iterator[str]:
    """Потокове читання файлу без завантаження всього вмісту в RAM."""
    with path.open("r", encoding="utf-8") as file:
        yield from file
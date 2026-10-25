from collections.abc import Iterable, Iterator
from itertools import islice
from typing import TypeVar

T = TypeVar("T")

def batched(iterable: Iterable[T], batch_size: int) -> Iterator[list[T]]:
    """Генераторне розбиття потоку на порції заданого розміру."""
    iterator = iter(iterable)
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            return
        yield batch
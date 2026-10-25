from collections.abc import Iterator
from typing import Any, Sequence

class ProductBatchIterator(Iterator):
    """Власний ітератор для послідовного проходження по колекції батчів."""
    def __init__(self, data: Sequence[Any], step: int) -> None:
        self._data = data
        self._step = max(1, step)
        self._index = 0

    def __iter__(self) -> "ProductBatchIterator":
        return self

    def __next__(self) -> Sequence[Any]:
        if self._index >= len(self._data):
            raise StopIteration
        batch = self._data[self._index : self._index + self._step]
        self._index += self._step
        return batch
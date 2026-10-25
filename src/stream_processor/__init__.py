"""
Пакет stream_processor для потокової обробки даних інтернет-магазину.
"""

from .models import ProductRecord
from .readers import stream_read_lines
from .parsers import parse_csv_rows
from .filters import (
    validate_products,
    filter_by_category,
    filter_low_stock,
    find_product,
)
from .transformations import normalize_product_names
from .batches import batched
from .analytics import calculate_inventory_statistics
from .iterators import ProductBatchIterator

__all__ = [
    "ProductRecord",
    "stream_read_lines",
    "parse_csv_rows",
    "validate_products",
    "filter_by_category",
    "filter_low_stock",
    "find_product",
    "normalize_product_names",
    "batched",
    "calculate_inventory_statistics",
    "ProductBatchIterator",
]
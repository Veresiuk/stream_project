import csv
import time
import tracemalloc
from pathlib import Path
from typing import Any, Callable

from .filters import validate_products
from .parsers import parse_csv_rows
from .readers import stream_read_lines

def run_eager(path: Path) -> int:
    """Eager-обробка: читання всього датасету в пам'ять."""
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        items = list(reader)  # Повна матеріалізація

    valid_items = []
    for row in items:
        try:
            p_id = int(row["product_id"])
            price = float(row["price"])
            qty = int(row["quantity"])
            if price >= 0 and qty >= 0:
                valid_items.append((p_id, price, qty))
        except (ValueError, KeyError):
            continue

    total_cost = sum(p * q for _, p, q in valid_items)
    return len(valid_items)

def run_lazy(path: Path) -> int:
    """Lazy-обробка: потокове читання та валідація."""
    lines = stream_read_lines(path)
    rows = parse_csv_rows(lines)
    valid_stream = validate_products(rows)

    # Generator expression для обчислення вартості без створення списку
    costs = (item.total_cost for item in valid_stream)
    total_cost = sum(costs)
    return 1

def measure_execution(func: Callable[[Path], Any], path: Path) -> tuple[float, float]:
    """Повертає (час_у_секундах, пікова_пам_ять_у_МБ)."""
    tracemalloc.start()
    start_time = time.perf_counter()

    func(path)

    elapsed_time = time.perf_counter() - start_time
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return elapsed_time, peak_memory / (1024 * 1024)
from itertools import accumulate, chain, islice
from pathlib import Path

from .analytics import calculate_inventory_statistics
from .batches import batched
from .benchmark import measure_execution, run_eager, run_lazy
from .filters import (
    filter_by_category,
    filter_low_stock,
    find_product,
    validate_products,
)
from .generator import generate_products_csv
from .models import ProductRecord
from .parsers import parse_csv_rows
from .readers import stream_read_lines
from .transformations import normalize_product_names

def build_stream_pipeline(path: Path):
    """Створення лінивого потокового конвеєра."""
    lines = stream_read_lines(path)
    rows = parse_csv_rows(lines)
    validated = validate_products(rows)
    normalized = normalize_product_names(validated)
    return normalized

def main() -> None:
    data_path = Path("data/products.csv")

    print("[1/5] Перевірка тестового датасету...")
    if not data_path.exists() or data_path.stat().st_size == 0:
        print("  Датасет відсутній або порожній. Генерація 100 000 записів...")
        generate_products_csv(data_path, count=100_000)
    print("  Файл готовий.\n")

    print("[2/5] Демонстрація базових вимог варіанта 3:")
    
    # Перші 3 товари з низьким залишком (<= 3) через islice
    pipeline = build_stream_pipeline(data_path)
    low_stock = filter_low_stock(pipeline, threshold=3)
    first_low_stock = list(islice(low_stock, 3))
    print(f"  Перші товари з низьким залишком (<= 3): {first_low_stock}")

    # Пошук за назвою або ID (ранній вихід)
    pipeline = build_stream_pipeline(data_path)
    found_item = find_product(pipeline, product_id=42)
    print(f"  Знайдений товар (ID=42): {found_item}")

    # Batch processing (порції по 2 товари для перших 5 записів)
    pipeline = build_stream_pipeline(data_path)
    batch_sample = list(islice(batched(pipeline, batch_size=2), 2))
    print(f"  Зразок перших 2 батчів: {batch_sample}\n")

    print("[3/5] Використання бібліотеки itertools:")
    pipe_a = filter_by_category(build_stream_pipeline(data_path), "Laptops")
    pipe_b = filter_by_category(build_stream_pipeline(data_path), "Audio")
    chained_stream = chain(islice(pipe_a, 2), islice(pipe_b, 2))
    print("  Товари з chain(Laptops, Audio):", [p.name for p in chained_stream])

    pipe_acc = build_stream_pipeline(data_path)
    sample_costs = (item.total_cost for item in islice(pipe_acc, 4))
    cumulative_costs = list(accumulate(sample_costs))
    print(f"  Кумулятивна сума перших 4 товарів (accumulate): {cumulative_costs}\n")

    print("[4/5] Потоковий розрахунок статистики (100 000 записів)...")
    pipeline = build_stream_pipeline(data_path)
    stats = calculate_inventory_statistics(pipeline)
    
    print(f"  Опрацьовано записів : {stats['records_count']}")
    print(f"  Загальна вартість   : {stats['total_inventory_cost']:,.2f} грн")
    print(f"  Загальна кількість  : {stats['total_quantity']} од.")
    if stats['most_expensive_product']:
        mep = stats['most_expensive_product']
        print(f"  Найдорожчий товар   : {mep.name} ({mep.price} грн)")
    print(f"  Категорій           : {len(stats['category_statistics'])}\n")

    print("[5/5] Порівняння Eager vs Lazy (час та споживання RAM):")
    eager_time, eager_mem = measure_execution(run_eager, data_path)
    lazy_time, lazy_mem = measure_execution(run_lazy, data_path)

    print(f"  {'Показник':<20} | {'Eager':<12} | {'Lazy':<12}")
    print(f"  {'-'*20}-+-{'-'*12}-+-{'-'*12}")
    print(f"  {'Час виконання (с)':<20} | {eager_time:<12.4f} | {lazy_time:<12.4f}")
    print(f"  {'Пікова RAM (МБ)':<20} | {eager_mem:<12.2f} | {lazy_mem:<12.2f}")

if __name__ == "__main__":
    main()
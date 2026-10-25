from collections import defaultdict
from collections.abc import Iterable
from typing import Any, Optional
from .models import ProductRecord

def calculate_inventory_statistics(products: Iterable[ProductRecord]) -> dict[str, Any]:
    """Streaming-обчислення загальної вартості, найдорожчого товару та статистики категорій."""
    total_inventory_cost = 0.0
    total_quantity = 0
    records_count = 0
    most_expensive_product: Optional[ProductRecord] = None
    
    category_stats: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"count": 0, "total_value": 0.0, "total_qty": 0}
    )

    for item in products:
        records_count += 1
        item_total = item.total_cost
        
        total_inventory_cost += item_total
        total_quantity += item.quantity

        if most_expensive_product is None or item.price > most_expensive_product.price:
            most_expensive_product = item

        cat = category_stats[item.category]
        cat["count"] += 1
        cat["total_value"] += item_total
        cat["total_qty"] += item.quantity

    return {
        "records_count": records_count,
        "total_inventory_cost": round(total_inventory_cost, 2),
        "total_quantity": total_quantity,
        "most_expensive_product": most_expensive_product,
        "category_statistics": dict(category_stats),
    }
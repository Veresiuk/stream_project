from collections.abc import Iterable, Iterator
from typing import Optional
from .models import ProductRecord

def validate_products(rows: Iterable[dict[str, str]]) -> Iterator[ProductRecord]:
    """Streaming validation ціни (price > 0) та кількості (quantity >= 0)."""
    for row in rows:
        try:
            p_id = int(row["product_id"])
            name = row["name"].strip()
            category = row["category"].strip()
            price = float(row["price"])
            quantity = int(row["quantity"])
        except (ValueError, TypeError, KeyError):
            continue

        if not name or not category:
            continue
        if price < 0 or quantity < 0:
            continue

        yield ProductRecord(
            product_id=p_id,
            name=name,
            category=category,
            price=price,
            quantity=quantity,
        )

def filter_by_category(products: Iterable[ProductRecord], category: str) -> Iterator[ProductRecord]:
    """Фільтрація товарів за категорією."""
    target = category.casefold()
    for product in products:
        if product.category.casefold() == target:
            yield product

def filter_low_stock(products: Iterable[ProductRecord], threshold: int = 5) -> Iterator[ProductRecord]:
    """Lazy-фільтрація товарів із низьким залишком."""
    for product in products:
        if product.quantity <= threshold:
            yield product

def find_product(
    products: Iterable[ProductRecord], 
    product_id: Optional[int] = None, 
    name: Optional[str] = None
) -> Optional[ProductRecord]:
    """Lazy-пошук товару з раннім перериванням (early termination)."""
    target_name = name.casefold() if name else None
    for product in products:
        if product_id is not None and product.product_id == product_id:
            return product
        if target_name is not None and product.name.casefold() == target_name:
            return product
    return None
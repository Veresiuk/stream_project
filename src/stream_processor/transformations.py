from collections.abc import Iterable, Iterator
from .models import ProductRecord

def normalize_product_names(products: Iterable[ProductRecord]) -> Iterator[ProductRecord]:
    """Нормалізація назв товарів та категорій."""
    for product in products:
        yield product._replace(
            name=product.name.strip().title(),
            category=product.category.strip().title(),
        )
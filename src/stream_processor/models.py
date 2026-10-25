from typing import NamedTuple

class ProductRecord(NamedTuple):
    product_id: int
    name: str
    category: str
    price: float
    quantity: int

    @property
    def total_cost(self) -> float:
        return round(self.price * self.quantity, 2)
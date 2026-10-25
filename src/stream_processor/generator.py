import csv
import random
from pathlib import Path

CATEGORIES = ["Laptops", "Smartphones", "Audio", "Monitors", "Keyboards", "Accessories"]
ADJECTIVES = ["Ultra", "Pro", "Lite", "Gaming", "Office", "Wireless", "Eco"]
NOUNS = ["Mouse", "Headset", "Screen", "Notebook", "Hub", "Keyboard", "Drive"]

def generate_products_csv(path: Path, count: int = 100_000) -> None:
    """Генерація CSV-файлу із заданою кількістю записів."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_id", "name", "category", "price", "quantity"])
        
        for idx in range(1, count + 1):
            name = f"{random.choice(ADJECTIVES)} {random.choice(NOUNS)} {random.randint(10, 999)}"
            category = random.choice(CATEGORIES)
            price = round(random.uniform(5.0, 3500.0), 2)
            quantity = random.randint(0, 100)
            writer.writerow([idx, name, category, price, quantity])
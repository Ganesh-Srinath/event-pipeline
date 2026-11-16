import json
import random
from datetime import datetime, timezone
from pathlib import Path

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

PRODUCTS = [
    {"id": "P101", "name": "Wireless Mouse", "price": 799.0},
    {"id": "P102", "name": "Mechanical Keyboard", "price": 2499.0},
    {"id": "P103", "name": "USB-C Hub", "price": 1299.0},
    {"id": "P104", "name": "Laptop Stand", "price": 999.0},
]
EVENT_TYPES = ["view", "add_to_cart", "purchase"]

def generate_batch(num_events: int = 500):
    events = []
    now = datetime.now(timezone.utc)
    for i in range(num_events):
        product = random.choice(PRODUCTS)
        event_type = random.choices(EVENT_TYPES, weights=[0.6, 0.25, 0.15])[0]
        # Inject ~20% dirty records (missing user_id or invalid quantity)
        is_dirty = random.random() < 0.20
        events.append({
            "event_id": f"EVT-{int(now.timestamp())}-{i}",
            "user_id": None if is_dirty else f"USR-{random.randint(1000, 1050)}",
            "product_id": product["id"],
            "product_name": product["name"],
            "event_type": event_type,
            "quantity": -1 if is_dirty else random.randint(1, 3),
            "unit_price": product["price"],
            "timestamp": now.isoformat(),
        })

    filename = RAW_DIR / f"shop_events_{now.strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2)
    print(f"Generated {len(events)} events in {filename}")

if __name__ == "__main__":
    generate_batch(random.randint(450, 550))
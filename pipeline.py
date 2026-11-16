import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from pymongo import MongoClient, UpdateOne

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

client = MongoClient("mongodb://localhost:27017/")
db = client["shop_analytics"]
raw_col = db["raw_events"]
clean_col = db["cleaned_events"]
summary_col = db["hourly_summary"]

def process_files():
    files = sorted(RAW_DIR.glob("*.json"))
    if not files:
        print("No new raw files to process.")
        return

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            records = json.load(f)

        if records:
            raw_col.insert_many(records)

        valid_records = []
        dropped = 0
        for r in records:
            if not r.get("user_id") or r.get("quantity", 0) <= 0:
                dropped += 1
                continue
            r["total_amount"] = round(r["quantity"] * r["unit_price"], 2)
            r["processed_at"] = datetime.now(timezone.utc).isoformat()
            valid_records.append(r)

        if valid_records:
            clean_col.insert_many(valid_records)

        # Aggregate hourly revenue & event counts
        purchases = [r for r in valid_records if r["event_type"] == "purchase"]
        revenue = round(sum(r["total_amount"] for r in purchases), 2)
        hour_bucket = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:00 UTC")

        summary_col.update_one(
            {"hour": hour_bucket},
            {
                "$inc": {
                    "total_raw": len(records),
                    "total_cleaned": len(valid_records),
                    "total_dropped": dropped,
                    "purchase_count": len(purchases),
                    "revenue": revenue,
                }
            },
            upsert=True,
        )

        shutil.move(str(file_path), str(PROCESSED_DIR / file_path.name))
        print(f"Processed {file_path.name}: {len(valid_records)} clean, {dropped} dropped, ₹{revenue} revenue")

if __name__ == "__main__":
    process_files()
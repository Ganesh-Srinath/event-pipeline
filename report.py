from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["shop_analytics"]

def print_report():
    print("\n=== SHOP PIPELINE SUMMARY REPORT ===")
    print(f"Raw Records Stored     : {db['raw_events'].count_documents({})}")
    print(f"Cleaned Records Stored : {db['cleaned_events'].count_documents({})}")
    print("\n--- Hourly Breakdown ---")
    for doc in db["hourly_summary"].find().sort("hour", -1):
        print(
            f"{doc['hour']} | Raw: {doc['total_raw']} | Clean: {doc['total_cleaned']} "
            f"| Dropped: {doc['total_dropped']} | Purchases: {doc['purchase_count']} "
            f"| Revenue: ₹{doc['revenue']:.2f}"
        )
    print("====================================\n")

if __name__ == "__main__":
    print_report()
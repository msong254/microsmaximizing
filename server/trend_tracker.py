import os
import json
from collections import defaultdict
from server.database.db import SessionLocal
from server.database.models.nutrient import Nutrient
from server.database.models.food_nutrient import FoodNutrient
from datetime import datetime

LOG_DIR = "logs"

def load_all_logs():
    logs = []
    for fname in sorted(os.listdir(LOG_DIR)):
        if fname.endswith(".json"):
            path = os.path.join(LOG_DIR, fname)
            with open(path) as f:
                data = json.load(f)
                date = fname.replace(".json", "")
                logs.append((date, data))
    return logs

def analyze_trend():
    session = SessionLocal()
    nutrient_meta = {n.id: n for n in session.query(Nutrient).all()}
    logs = load_all_logs()
    daily_totals = {}

    for date, entries in logs:
        totals = defaultdict(float)
        for entry in entries:
            food_id = entry["fdc_id"]
            grams = entry["grams"]

            rows = session.query(FoodNutrient).filter(
                FoodNutrient.food_id == food_id
            ).all()

            for row in rows:
                totals[row.nutrient_id] += row.amount * (grams / 100)
        
        daily_totals[date] = totals

    print("\n📊 % of RDA per day (major nutrients):\n")

    tracked_names = ["Calories", "Protein", "Vitamin C", "Iron", "Calcium", "Fiber", "Vitamin D"]
    tracked_ids = [
        nid for nid, n in nutrient_meta.items()
        if any(k.lower() in n.name.lower() for k in tracked_names)
    ]

    # Print table header
    print("Date".ljust(12), end="")
    for nid in tracked_ids:
        print(nutrient_meta[nid].name[:12].ljust(14), end="")
    print()

    # Print rows
    for date, totals in daily_totals.items():
        print(date.ljust(12), end="")
        for nid in tracked_ids:
            rda = nutrient_meta[nid].rda
            total = totals.get(nid, 0)
            if rda > 0:
                percent = total / rda * 100
                flag = "!" if percent < 90 else ""
                print(f"{percent:.0f}%{flag}".ljust(14), end="")
            else:
                print("-".ljust(14), end="")
        print()

    session.close()

if __name__ == "__main__":
    analyze_trend()
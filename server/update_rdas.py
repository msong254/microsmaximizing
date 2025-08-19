import json
import os
from datetime import date
from collections import defaultdict

from server.database.db import SessionLocal
from server.database.models.food_nutrient import FoodNutrient
from server.database.models.nutrient import Nutrient

LOG_DIR = "logs"

def load_today_log():
    today = date.today().isoformat()
    path = os.path.join(LOG_DIR, f"{today}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def analyze():
    log = load_today_log()
    if not log:
        print("❌ No foods logged today.")
        return

    session = SessionLocal()
    totals = defaultdict(float)
    nutrient_meta = {}

    for entry in log:
        food_id = entry["fdc_id"]
        grams = entry["grams"]

        rows = session.query(FoodNutrient, Nutrient).join(
            Nutrient, FoodNutrient.nutrient_id == Nutrient.id
        ).filter(FoodNutrient.food_id == food_id).all()

        for fn, n in rows:
            amount = fn.amount * (grams / 100)
            totals[n.id] += amount
            nutrient_meta[n.id] = {
                "name": n.name,
                "unit": n.unit,
                "rda": n.rda
            }

    print(f"\n📊 Total nutrient intake for {date.today().isoformat()}:\n")

    for nutrient_id, total in sorted(totals.items(), key=lambda x: nutrient_meta[x[0]]["name"].lower()):
        meta = nutrient_meta[nutrient_id]
        rda = meta["rda"]
        unit = meta["unit"]
        name = meta["name"]

        if rda > 0:
            percent = (total / rda) * 100
            status = f"{percent:.0f}% of RDA"
            flag = "⚠️ LOW" if percent < 90 else ""
        else:
            status = "No RDA"
            flag = ""

        print(f"{name}: {total:.2f} {unit} – {status} {flag}")

    session.close()

if __name__ == "__main__":
    analyze()
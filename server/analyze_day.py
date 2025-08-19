import json
import os
from datetime import date
from collections import defaultdict

from server.database.db import SessionLocal
from server.database.models.food_nutrient import FoodNutrient
from server.database.models.nutrient import Nutrient

LOG_DIR = "logs"

# Nutrient names we care about (match partial strings)
tracked_keywords = [
    "Calories", "Energy", "Protein", "Carbohydrate", "Fiber",
    "Fat", "Saturated", "Trans", "Cholesterol",
    "Calcium", "Iron", "Magnesium", "Phosphorus", "Potassium",
    "Sodium", "Zinc", "Vitamin A", "Vitamin C", "Vitamin D",
    "Vitamin E", "Vitamin K", "Thiamin", "Riboflavin", "Niacin",
    "Vitamin B6", "Folate", "Vitamin B12"
]

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

    # Step 1: Get nutrients we care about
    nutrients = session.query(Nutrient).all()
    tracked_nutrients = {
        n.id: n for n in nutrients if any(k.lower() in n.name.lower() for k in tracked_keywords)
    }

    totals = {nid: 0.0 for nid in tracked_nutrients}
    
    # Step 2: Tally all nutrient intake
    for entry in log:
        food_id = entry["fdc_id"]
        grams = entry["grams"]

        rows = session.query(FoodNutrient).filter(
            FoodNutrient.food_id == food_id,
            FoodNutrient.nutrient_id.in_(tracked_nutrients.keys())
        ).all()

        for row in rows:
            totals[row.nutrient_id] += row.amount * (grams / 100)

    # Step 3: Print everything (even 0 totals)
    print(f"\n📊 Total nutrient intake for {date.today().isoformat()}:\n")

    for nid, nutrient in sorted(tracked_nutrients.items(), key=lambda x: x[1].name.lower()):
        total = totals[nid]
        rda = nutrient.rda
        unit = nutrient.unit

        if rda > 0:
            percent = (total / rda) * 100
            status = f"{percent:.0f}% of RDA"
            flag = "⚠️ LOW" if percent < 90 else ""
        else:
            status = "No RDA"
            flag = ""

        print(f"{nutrient.name}: {total:.2f} {unit} – {status} {flag}")

    session.close()

if __name__ == "__main__":
    analyze()
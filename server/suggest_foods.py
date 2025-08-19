import json
import os
from datetime import date
from collections import defaultdict

from server.database.db import SessionLocal
from server.database.models.food import Food
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

def get_deficiencies():
    log = load_today_log()
    if not log:
        print("❌ No foods logged today.")
        return {}

    session = SessionLocal()
    totals = defaultdict(float)
    rdas = {}
    nutrient_names = {}

    for entry in log:
        food_id = entry["fdc_id"]
        grams = entry["grams"]

        rows = session.query(FoodNutrient, Nutrient).join(
            Nutrient, FoodNutrient.nutrient_id == Nutrient.id
        ).filter(FoodNutrient.food_id == food_id).all()

        for fn, n in rows:
            amount = fn.amount * (grams / 100)
            totals[n.id] += amount
            rdas[n.id] = n.rda
            nutrient_names[n.id] = n.name

    deficiencies = {}
    for nid, rda in rdas.items():
        if rda > 0 and totals[nid] < rda * 0.9:
            deficiencies[nid] = {
                "name": nutrient_names[nid],
                "amount": totals[nid],
                "rda": rda,
                "deficit": rda - totals[nid]
            }

    session.close()
    return deficiencies

def suggest_foods_for_deficiency(nutrient_id, session, limit=5):
    results = session.query(
        Food.name, FoodNutrient.amount
    ).join(FoodNutrient, Food.id == FoodNutrient.food_id
    ).filter(FoodNutrient.nutrient_id == nutrient_id
    ).order_by(FoodNutrient.amount.desc()).limit(limit).all()

    return results

def main():
    session = SessionLocal()
    deficiencies = get_deficiencies()

    if not deficiencies:
        print("✅ No major deficiencies detected.")
        return

    print(f"\n🥗 Food suggestions to fix today's deficiencies:\n")

    for nid, info in deficiencies.items():
        print(f"⚠️ {info['name']} – {info['amount']:.2f} / {info['rda']} ({info['deficit']:.2f} deficit)")
        suggestions = suggest_foods_for_deficiency(nid, session)
        for food, amount in suggestions:
            print(f"   • {food} — {amount:.2f} per 100g")
        print()

    session.close()

if __name__ == "__main__":
    main()
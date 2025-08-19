import json
import os
from datetime import date

from server.database.db import SessionLocal
from server.database.models.food import Food
from server.database.models.nutrient import Nutrient
from server.database.models.food_nutrient import FoodNutrient

LOG_DIR = "logs"

def get_food_by_keyword(session, keyword):
    return session.query(Food).filter(Food.name.ilike(f"%{keyword}%")).limit(10).all()

def get_nutrients_for_food(session, food_id):
    results = session.query(
        FoodNutrient, Nutrient
    ).join(Nutrient, FoodNutrient.nutrient_id == Nutrient.id).filter(FoodNutrient.food_id == food_id).all()
    
    nutrient_totals = {}
    for fn, n in results:
        nutrient_totals[n.name] = {
            "amount": fn.amount,
            "unit": n.unit,
            "rda": n.rda
        }
    return nutrient_totals

def load_today_log():
    today = date.today().isoformat()
    path = os.path.join(LOG_DIR, f"{today}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_today_log(data):
    today = date.today().isoformat()
    path = os.path.join(LOG_DIR, f"{today}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    session = SessionLocal()
    log = load_today_log()

    food_input = input("🍽️  What food did you eat? ").strip()
    results = get_food_by_keyword(session, food_input)

    if not results:
        print("❌ No matching foods found.")
        return

    print("\n🔍 Matching foods:")
    for i, food in enumerate(results):
        print(f"{i + 1}. {food.name} (FDC ID: {food.id})")

    index = int(input("\nSelect a food (1-10): ")) - 1
    food = results[index]
    quantity = float(input("How many grams did you eat? "))

    log.append({"fdc_id": food.id, "name": food.name, "grams": quantity})
    save_today_log(log)
    print(f"\n✅ Logged {quantity}g of {food.name}.\n")

    # Optional: Show nutrients right away
    nutrients = get_nutrients_for_food(session, food.id)
    print("📊 Nutrients in this portion:")
    for name, info in nutrients.items():
        scaled = info["amount"] * (quantity / 100)
        print(f"{name}: {scaled:.2f} {info['unit']}")

    session.close()

if __name__ == "__main__":
    main()
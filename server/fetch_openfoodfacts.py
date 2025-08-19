import requests
from server.database.db import SessionLocal
from server.database.models.food import Food
from server.database.models.nutrient import Nutrient
from server.database.models.food_nutrient import FoodNutrient

def insert_product(db, product):
    name = product.get("product_name", "").strip()
    if not name:
        return

    # Skip if already inserted
    if db.query(Food).filter(Food.name == name).first():
        return

    nutriments = product.get("nutriments", {})
    if not nutriments:
        return

    food = Food(name=name)
    db.add(food)
    db.flush()

    for key, value in nutriments.items():
        if "_100g" not in key:
            continue

        nutrient_name = key.replace("_100g", "").replace("_", " ").title()
        unit = nutriments.get(f"{key}_unit", "")

        nutrient = db.query(Nutrient).filter(Nutrient.name == nutrient_name).first()
        if not nutrient:
            nutrient = Nutrient(name=nutrient_name, unit=unit)
            db.add(nutrient)
            db.flush()

        try:
            amount = float(value)
        except ValueError:
            continue

        food_nutrient = FoodNutrient(
            food_id=food.id,
            nutrient_id=nutrient.id,
            amount=amount
        )
        db.add(food_nutrient)

    db.commit()
    print(f"✅ Inserted: {name}")


def seed_openfoodfacts():
    db = SessionLocal()
    page = 1
    max_pages = 1000  # Adjust if needed

    while page <= max_pages:
        print(f"\n📦 Fetching page {page}...")
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "page": page,
            "page_size": 1000,
            "search_simple": 1,
            "action": "process",
            "json": 1,
        }

        res = requests.get(url, params=params)
        data = res.json()
        products = data.get("products", [])

        if not products:
            break

        for product in products:
            insert_product(db, product)

        page += 1

    db.close()
    print("🎉 Done seeding all OpenFoodFacts data.")

if __name__ == "__main__":
    seed_openfoodfacts()
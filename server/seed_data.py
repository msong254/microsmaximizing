import csv
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models.food import Food
from database.models.nutrient import Nutrient
from database.models.food_nutrient import FoodNutrient

FOOD_CSV = "usda_data/Food.csv"
NUTRIENT_CSV = "usda_data/Nutrient.csv"
FOOD_NUTRIENT_CSV = "usda_data/food_nutrient.csv"

def seed_foods(session: Session):
    print("Seeding foods...")
    with open(FOOD_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        foods = []
        for i, row in enumerate(reader, start=1):
            foods.append(Food(id=int(row["fdc_id"]), name=row["description"]))
            if i % 1000 == 0:
                print(f"  Processed {i} foods...")
        session.bulk_save_objects(foods)
        session.commit()
    print("✅ Done seeding foods.")

def seed_nutrients(session: Session):
    print("Seeding nutrients...")
    with open(NUTRIENT_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        nutrients = []
        for i, row in enumerate(reader, start=1):
            nutrients.append(Nutrient(
                id=int(row["id"]),
                name=row["name"],
                unit=row["unit_name"]
            ))
            if i % 500 == 0:
                print(f"  Processed {i} nutrients...")
        session.bulk_save_objects(nutrients)
        session.commit()
    print("✅ Done seeding nutrients.")

def seed_food_nutrients(session: Session):
    print("Seeding food nutrients...")
    with open(FOOD_NUTRIENT_CSV, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        batch = []
        for i, row in enumerate(reader, start=1):
            amount = float(row["amount"]) if row["amount"] else 0.0
            fn = FoodNutrient(
                food_id=int(row["fdc_id"]),
                nutrient_id=int(row["nutrient_id"]),
                amount=amount
            )
            batch.append(fn)

            if i % 10000 == 0:
                session.bulk_save_objects(batch)
                session.commit()
                batch = []
                print(f"  Inserted {i} food_nutrient rows...")

        if batch:
            session.bulk_save_objects(batch)
            session.commit()
    print("✅ Done seeding food nutrients.")

def seed():
    session = SessionLocal()
    seed_foods(session)
    seed_nutrients(session)
    seed_food_nutrients(session)
    session.close()

if __name__ == "__main__":
    seed()
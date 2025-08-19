# server/seed_rda.py

from database.db import SessionLocal
from database.models.rda import RDA

rda_values = [
    {"nutrient_id": 1003, "value": 56, "unit": "G"},       # Protein
    {"nutrient_id": 1004, "value": 78, "unit": "G"},       # Total Fat
    {"nutrient_id": 1005, "value": 275, "unit": "G"},      # Carbohydrate
    {"nutrient_id": 1079, "value": 38, "unit": "G"},       # Fiber
    {"nutrient_id": 1087, "value": 1300, "unit": "MG"},    # Calcium
    {"nutrient_id": 1089, "value": 18, "unit": "MG"},      # Iron
    {"nutrient_id": 1093, "value": 2300, "unit": "MG"},    # Sodium
    {"nutrient_id": 1106, "value": 90, "unit": "MG"},      # Vitamin C
    {"nutrient_id": 1110, "value": 900, "unit": "UG"},     # Vitamin A
    {"nutrient_id": 1114, "value": 15, "unit": "UG"},      # Vitamin D
]

def seed_rda():
    db = SessionLocal()
    for item in rda_values:
        exists = db.query(RDA).filter_by(nutrient_id=item["nutrient_id"]).first()
        if not exists:
            db.add(RDA(**item))
    db.commit()
    db.close()
    print("✅ Done seeding RDA values.")

if __name__ == "__main__":
    seed_rda()
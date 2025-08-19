# scripts/seed_rda.py

from server.database.db import SessionLocal
from server.database.models.nutrient import Nutrient

rda_data = {
    "Vitamin D": 20,
    "Vitamin C": 90,
    "Calcium, Ca": 1000,
    "Iron, Fe": 18,
    "Magnesium, Mg": 400,
    "Zinc, Zn": 11,
    "Vitamin A": 900,
    "Protein": 56,
}

db = SessionLocal()

for name, amount in rda_data.items():
    nutrient = db.query(Nutrient).filter(Nutrient.name.ilike(f"%{name}%")).first()
    if nutrient:
        nutrient.rda = amount
        db.add(nutrient)

db.commit()
db.close()
print("✅ RDA values seeded into `nutrients` table.")
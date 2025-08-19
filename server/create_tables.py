from database.db import Base, engine

# Import ALL models so Base.metadata.create_all() sees them
from database.models.food import Food
from database.models.nutrient import Nutrient
from database.models.food_nutrient import FoodNutrient
from database.models.log import FoodLog
from database.models.user import User
from database.models.rda import RDA  # ✅ fixed this line

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
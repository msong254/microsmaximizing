from sqlalchemy import Column, Integer, ForeignKey, Float
from database.db import Base  # ❌ FIXED import

class FoodNutrient(Base):
    __tablename__ = "food_nutrients"
    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"))
    nutrient_id = Column(Integer, ForeignKey("nutrients.id"))
    amount = Column(Float)
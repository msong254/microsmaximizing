from sqlalchemy import Column, Integer, Float, ForeignKey, Date
from database.db import Base

class FoodLog(Base):
    __tablename__ = "food_logs"
    id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"))
    amount = Column(Float)
    log_date = Column(Date)
from sqlalchemy import Column, Integer, String
from database.db import Base  # ❌ FIXED import

class Food(Base):
    __tablename__ = "foods"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
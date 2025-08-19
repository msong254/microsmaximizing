from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class RDA(Base):
    __tablename__ = "rda"

    id = Column(Integer, primary_key=True, index=True)
    nutrient_id = Column(Integer, ForeignKey("nutrients.id"), unique=True)
    value = Column(Float)
    unit = Column(String)

    nutrient = relationship("Nutrient", back_populates="rda")
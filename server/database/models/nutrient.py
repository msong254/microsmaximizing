from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base

class Nutrient(Base):
    __tablename__ = "nutrients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    unit = Column(String)

    rda = relationship("database.models.rda.RDA", back_populates="nutrient", uselist=False)
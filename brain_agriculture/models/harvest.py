# brain_agriculture/models/harvest.py

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from brain_agriculture.models.base import Base

class Harvest(Base):
    __tablename__ = "harvests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    farm = relationship("Farm", back_populates="harvests")
    harvest_crops = relationship("HarvestCrop", back_populates="harvest", cascade="all, delete")

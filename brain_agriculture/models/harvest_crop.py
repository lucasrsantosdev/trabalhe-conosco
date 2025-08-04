# brain_agriculture/models/harvest_crop.py

from sqlalchemy import Column, Integer, ForeignKey, Float
from brain_agriculture.models.base import Base
from sqlalchemy.orm import relationship

class HarvestCrop(Base):
    __tablename__ = "harvest_crops"

    id = Column(Integer, primary_key=True, index=True)
    harvest_id = Column(Integer, ForeignKey("harvests.id"))
    crop_id = Column(Integer, ForeignKey("crops.id"))
    quantity = Column(Float, nullable=False)

    harvest = relationship("Harvest", back_populates="harvest_crops")
    crop = relationship("Crop", back_populates="harvest_crops")

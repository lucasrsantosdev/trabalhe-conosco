from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class HarvestCrop(Base):
    __tablename__ = "harvest_crops"

    id = Column(Integer, primary_key=True, index=True)
    harvest_id = Column(Integer, ForeignKey("harvests.id"))
    crop_id = Column(Integer, ForeignKey("crops.id"))

    harvest = relationship("Harvest", back_populates="harvest_crops")
    crop = relationship("Crop", back_populates="harvest_crops")

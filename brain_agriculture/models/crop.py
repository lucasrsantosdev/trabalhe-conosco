# brain_agriculture/models/crop.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from brain_agriculture.models.base import Base


class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    variety = Column(String, nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    farm = relationship("Farm", back_populates="crops")
    harvest_crops = relationship("HarvestCrop", back_populates="crop", cascade="all, delete")

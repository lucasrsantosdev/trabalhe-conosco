from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Harvest(Base):
    __tablename__ = "harvests"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(String, nullable=False)

    farm_id = Column(Integer, ForeignKey("farms.id"))
    farm = relationship("Farm", back_populates="harvests")

    harvest_crops = relationship("HarvestCrop", back_populates="harvest", cascade="all, delete-orphan")

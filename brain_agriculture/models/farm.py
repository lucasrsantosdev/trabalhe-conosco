from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from brain_agriculture.models.base import Base

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    total_area = Column(Float, nullable=False)
    agricultural_area = Column(Float, nullable=False)
    vegetation_area = Column(Float, nullable=False)
    
    producer_id = Column(Integer, ForeignKey("producers.id"), nullable=False)

    producer = relationship("Producer", back_populates="farms")
    crops = relationship("Crop", back_populates="farm", cascade="all, delete")

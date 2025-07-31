from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    area_total = Column(Float, nullable=False)
    area_agricultural = Column(Float, nullable=False)
    area_vegetation = Column(Float, nullable=False)

    producer_id = Column(Integer, ForeignKey("producers.id"))
    producer = relationship("Producer", back_populates="farms")

    harvests = relationship("Harvest", back_populates="farm", cascade="all, delete-orphan")

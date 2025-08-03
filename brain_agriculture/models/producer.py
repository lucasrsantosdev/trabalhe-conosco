from sqlalchemy import Column, Integer, String
from brain_agriculture.models.base import Base

class Producer(Base):
    __tablename__ = "producers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    document = Column(String, unique=True, nullable=False)

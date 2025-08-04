from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from brain_agriculture import database
from brain_agriculture.models import producer as models
from brain_agriculture.schemas.producer import ProducerCreate, ProducerFullCreate, Producer

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/producers", response_model=Producer)
def create_producer(producer: ProducerCreate, db: Session = Depends(get_db)):
    db_producer = models.Producer(**producer.dict())
    db.add(db_producer)
    db.commit()
    db.refresh(db_producer)
    return db_producer

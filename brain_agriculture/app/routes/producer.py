# brain_agriculture/app/routes/producer.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from brain_agriculture.database import SessionLocal
from brain_agriculture import schemas, models

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/producers", response_model=schemas.producer.Producer)
def create_producer(producer: schemas.producer.ProducerCreate, db: Session = Depends(get_db)):
    db_producer = models.producer.Producer(**producer.dict())
    db.add(db_producer)
    db.commit()
    db.refresh(db_producer)
    return db_producer

@router.get("/producers", response_model=list[schemas.producer.Producer])
def get_producers(db: Session = Depends(get_db)):
    return db.query(models.producer.Producer).all()

@router.get("/producers/{producer_id}", response_model=schemas.producer.Producer)
def get_producer(producer_id: int, db: Session = Depends(get_db)):
    producer = db.query(models.producer.Producer).get(producer_id)
    if not producer:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    return producer

@router.put("/producers/{producer_id}", response_model=schemas.producer.Producer)
def update_producer(producer_id: int, updated: schemas.producer.ProducerCreate, db: Session = Depends(get_db)):
    producer = db.query(models.producer.Producer).get(producer_id)
    if not producer:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    for key, value in updated.dict().items():
        setattr(producer, key, value)
    db.commit()
    db.refresh(producer)
    return producer

@router.delete("/producers/{producer_id}")
def delete_producer(producer_id: int, db: Session = Depends(get_db)):
    producer = db.query(models.producer.Producer).get(producer_id)
    if not producer:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    db.delete(producer)
    db.commit()
    return {"detail": "Produtor deletado com sucesso"}

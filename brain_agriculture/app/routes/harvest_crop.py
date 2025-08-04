# brain_agriculture/app/routes/harvest.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from brain_agriculture import database
from brain_agriculture.models import harvest as harvest_model
from brain_agriculture.schemas import harvest as harvest_schema

router = APIRouter(prefix="/harvests", tags=["Harvests"])

@router.post("/", response_model=harvest_schema.Harvest)
def create_harvest(harvest: harvest_schema.HarvestCreate, db: Session = Depends(database.get_db)):
    db_harvest = harvest_model.Harvest(**harvest.dict())
    db.add(db_harvest)
    db.commit()
    db.refresh(db_harvest)
    return db_harvest

@router.get("/", response_model=list[harvest_schema.Harvest])
def list_harvests(db: Session = Depends(database.get_db)):
    return db.query(harvest_model.Harvest).all()

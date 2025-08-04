# brain_agriculture/app/routes/crop.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from brain_agriculture.database import get_db
from brain_agriculture.models.crop import Crop as CropModel
from brain_agriculture.schemas.crop import CropCreate, Crop

router = APIRouter()

@router.post("/crops", response_model=Crop)
def create_crop(crop: CropCreate, db: Session = Depends(get_db)):
    db_crop = CropModel(**crop.dict())
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    return db_crop

@router.get("/crops", response_model=list[Crop])
def read_crops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(CropModel).offset(skip).limit(limit).all()

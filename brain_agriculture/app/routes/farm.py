from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from brain_agriculture.database import get_db
from brain_agriculture.models.farm import Farm as FarmModel
from brain_agriculture.schemas.farm import Farm, FarmCreate, FarmUpdate

router = APIRouter()

@router.get("/farms", response_model=list[Farm])
def read_farms(db: Session = Depends(get_db)):
    return db.query(FarmModel).all()

@router.post("/farms", response_model=Farm)
def create_farm(farm: FarmCreate, db: Session = Depends(get_db)):
    db_farm = FarmModel(**farm.dict())
    db.add(db_farm)
    db.commit()
    db.refresh(db_farm)
    return db_farm

@router.put("/farms/{farm_id}", response_model=Farm)
def update_farm(farm_id: int, farm: FarmUpdate, db: Session = Depends(get_db)):
    db_farm = db.query(FarmModel).filter(FarmModel.id == farm_id).first()
    if db_farm is None:
        raise HTTPException(status_code=404, detail="Farm not found")
    for key, value in farm.dict().items():
        setattr(db_farm, key, value)
    db.commit()
    db.refresh(db_farm)
    return db_farm

@router.delete("/farms/{farm_id}")
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    db_farm = db.query(FarmModel).filter(FarmModel.id == farm_id).first()
    if db_farm is None:
        raise HTTPException(status_code=404, detail="Farm not found")
    db.delete(db_farm)
    db.commit()
    return {"detail": "Farm deleted"}

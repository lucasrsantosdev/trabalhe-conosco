from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from brain_agriculture import database
from brain_agriculture.models import farm as FarmModel
from brain_agriculture.models import producer as ProducerModel
from brain_agriculture.models import crop as CropModel
from brain_agriculture.models import harvest as HarvestModel
from brain_agriculture.models import harvest_crop as HCModel

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/totals")
def totals(db: Session = Depends(get_db)):
    total_farms = db.query(func.count(FarmModel.Farm.id)).scalar() or 0
    total_hectares = db.query(func.coalesce(func.sum(FarmModel.Farm.area_total), 0.0)).scalar() or 0.0
    return {"total_farms": total_farms, "total_hectares": float(total_hectares)}

@router.get("/pie-by-state")
def pie_by_state(db: Session = Depends(get_db)):
    rows = (
        db.query(FarmModel.Farm.state, func.count(FarmModel.Farm.id))
          .group_by(FarmModel.Farm.state)
          .all()
    )
    return [{"state": s, "farms": c} for s, c in rows]

@router.get("/pie-by-crop")
def pie_by_crop(db: Session = Depends(get_db)):
    # número de vínculos safra-cultura por cultura (ou distinct farms se preferir)
    rows = (
        db.query(CropModel.Crop.name, func.count(HCModel.HarvestCrop.id))
          .join(HCModel.HarvestCrop, HCModel.HarvestCrop.crop_id == CropModel.Crop.id)
          .group_by(CropModel.Crop.name)
          .all()
    )
    return [{"crop": name, "count": count} for name, count in rows]

@router.get("/pie-land-use")
def pie_land_use(db: Session = Depends(get_db)):
    sums = db.query(
        func.coalesce(func.sum(FarmModel.Farm.area_agricultavel), 0.0),
        func.coalesce(func.sum(FarmModel.Farm.area_vegetacao), 0.0),
    ).one()
    return {
        "agricultavel": float(sums[0]),
        "vegetacao": float(sums[1]),
    }

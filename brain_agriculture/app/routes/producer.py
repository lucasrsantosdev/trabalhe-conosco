# Caminho: brain_agriculture/app/routes/producer.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from brain_agriculture import database
from brain_agriculture.models import producer as models
from brain_agriculture.schemas.producer import ProducerCreate, ProducerFullCreate, Producer

router = APIRouter()

# ✅ ADICIONE ISSO LOGO AQUI
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/producer-full", status_code=201)
def create_producer_full(producer_data: ProducerFullCreate, db: Session = Depends(get_db)):
    # 1. Criar produtor
    producer = models.Producer(
        cpf_cnpj=producer_data.document,
        name=producer_data.name
    )
    db.add(producer)
    db.commit()
    db.refresh(producer)

    # 2. Criar fazenda
    farm_data = producer_data.farm
    farm = farm_models.Farm(
        name=farm_data.name,
        city=farm_data.city,
        state=farm_data.state,
        total_area=farm_data.total_area,
        arable_area=farm_data.arable_area,
        vegetation_area=farm_data.vegetation_area,
        producer_id=producer.id
    )
    db.add(farm)
    db.commit()
    db.refresh(farm)

    # 3. Criar safras e culturas
    for harvest_data in farm_data.harvests:
        harvest = harvest_models.Harvest(
            year=harvest_data.year,
            farm_id=farm.id
        )
        db.add(harvest)
        db.commit()
        db.refresh(harvest)

        for crop_data in harvest_data.crops:
            # Verifica se a cultura já existe, senão cria
            crop = db.query(crop_models.Crop).filter_by(name=crop_data.crop_name).first()
            if not crop:
                crop = crop_models.Crop(name=crop_data.crop_name)
                db.add(crop)
                db.commit()
                db.refresh(crop)

            # Cria a associação entre safra e cultura
            harvest_crop = hc_models.HarvestCrop(
                harvest_id=harvest.id,
                crop_id=crop.id
            )
            db.add(harvest_crop)

    db.commit()
    return {"message": "Produtor completo criado com sucesso"}

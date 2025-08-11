# brain_agriculture/app/routes/producer.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from brain_agriculture import database
from brain_agriculture.models import producer as producer_models
from brain_agriculture.models import farm as farm_models
from brain_agriculture.models import harvest as harvest_models
from brain_agriculture.models import harvest_crop as hc_models
from brain_agriculture.models import crop as crop_models

from brain_agriculture.schemas.producer import (
    ProducerCreate,
    Producer,
    ProducerFullCreate,
)

router = APIRouter(tags=["Producers"])


# --- DB dependency ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- CREATE: produtor + fazendas + safras + culturas ---
@router.post("/producer-full", status_code=201)
def create_producer_full(producer_data: ProducerFullCreate, db: Session = Depends(get_db)):
    # 1) Produtor
    new_producer = producer_models.Producer(
        cpf_cnpj=producer_data.cpf_cnpj,
        name=producer_data.name,
    )
    db.add(new_producer)
    db.flush()  # garante ID

    # 2) Fazendas, 3) Safras, 4) Culturas
    for farm_data in producer_data.farms:
        new_farm = farm_models.Farm(
            name=farm_data.name,
            city=farm_data.city,
            state=farm_data.state,
            area_total=farm_data.area_total,
            area_agricultavel=farm_data.area_agricultavel,
            area_vegetacao=farm_data.area_vegetacao,
            producer_id=new_producer.id,
        )
        db.add(new_farm)
        db.flush()

        for harvest_data in farm_data.harvests:
            new_harvest = harvest_models.Harvest(
                name=f"Safra {harvest_data.year}",
                start_date=f"{harvest_data.year}-01-01",
                end_date=f"{harvest_data.year}-12-31",
                farm_id=new_farm.id,
            )
            db.add(new_harvest)
            db.flush()

            for crop_data in harvest_data.crops:
                crop = db.query(crop_models.Crop).filter_by(name=crop_data.crop_name).first()
                if not crop:
                    crop = crop_models.Crop(name=crop_data.crop_name)
                    db.add(crop)
                    db.flush()

                db.add(hc_models.HarvestCrop(
                    harvest_id=new_harvest.id,
                    crop_id=crop.id,
                    quantity=0  # ajuste se desejar
                ))

    db.commit()
    return {"message": "Produtor, fazendas, safras e culturas cadastrados com sucesso"}


# --- READ: lista simples de produtores ---
@router.get("/producers", response_model=list[Producer])
def list_producers(db: Session = Depends(get_db)):
    return db.query(producer_models.Producer).all()


# --- UPDATE ---
@router.put("/producers/{producer_id}", response_model=Producer)
def update_producer(producer_id: int, data: ProducerCreate, db: Session = Depends(get_db)):
    obj = db.query(producer_models.Producer).get(producer_id)
    if not obj:
        raise HTTPException(404, "Produtor não encontrado")

    # checa duplicidade de CPF/CNPJ ao trocar
    if data.cpf_cnpj != obj.cpf_cnpj:
        exists = db.query(producer_models.Producer).filter(
            producer_models.Producer.cpf_cnpj == data.cpf_cnpj
        ).first()
        if exists:
            raise HTTPException(400, "CPF/CNPJ já cadastrado")

    obj.cpf_cnpj = data.cpf_cnpj
    obj.name = data.name
    db.commit()
    db.refresh(obj)
    return obj


# --- DELETE ---
@router.delete("/producers/{producer_id}", status_code=204)
def delete_producer(producer_id: int, db: Session = Depends(get_db)):
    obj = db.query(producer_models.Producer).get(producer_id)
    if not obj:
        raise HTTPException(404, "Produtor não encontrado")
    db.delete(obj)
    db.commit()

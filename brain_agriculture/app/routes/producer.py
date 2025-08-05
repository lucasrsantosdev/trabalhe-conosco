# Caminho: brain_agriculture/app/routes/producer.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from brain_agriculture import database
from brain_agriculture.models import producer as models
from brain_agriculture.models import farm as farm_models
from brain_agriculture.models import harvest as harvest_models
from brain_agriculture.models import harvest_crop as hc_models
from brain_agriculture.models import crop as crop_models

from brain_agriculture.schemas.producer import ProducerFullCreate
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
    # 1. Cria o produtor
    new_producer = models.Producer(
        cpf_cnpj=producer_data.document,
        name=producer_data.name
    )
    db.add(new_producer)
    db.flush()  # Para garantir que o ID do produtor seja gerado

    for farm_data in producer_data.farms:
        # 2. Cria a fazenda
        new_farm = farm_models.Farm(
            name=farm_data.name,
            city=farm_data.city,
            state=farm_data.state,
            area_total=farm_data.area_total,
            area_agricultavel=farm_data.area_agricultavel,
            area_vegetacao=farm_data.area_vegetacao,
            producer_id=new_producer.id
        )
        db.add(new_farm)
        db.flush()  # Gera o ID da fazenda

        for harvest_data in farm_data.harvests:
            # 3. Cria a safra
            new_harvest = harvest_models.Harvest(
                name=f"Safra {harvest_data.year}",
                start_date=f"{harvest_data.year}-01-01",
                end_date=f"{harvest_data.year}-12-31",
                farm_id=new_farm.id
            )
            db.add(new_harvest)
            db.flush()  # Gera o ID da safra

            for crop_data in harvest_data.crops:
                # Verifica se a cultura já existe
                existing_crop = db.query(crop_models.Crop).filter_by(name=crop_data.crop_name).first()
                if not existing_crop:
                    existing_crop = crop_models.Crop(name=crop_data.crop_name)
                    db.add(existing_crop)
                    db.flush()

                # 4. Associa a cultura à safra
                new_harvest_crop = hc_models.HarvestCrop(
                    harvest_id=new_harvest.id,
                    crop_id=existing_crop.id,
                    quantity=0  # Ajuste se quiser permitir informar quantidade
                )
                db.add(new_harvest_crop)

    db.commit()
    return {"message": "Produtor, fazendas, safras e culturas cadastrados com sucesso"}

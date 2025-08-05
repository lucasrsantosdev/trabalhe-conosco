from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from brain_agriculture.schemas.harvest_crop import HarvestCropCreate  # IMPORT NECESSÁRIO

class HarvestBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    farm_id: int

class HarvestCreate(HarvestBase):
    crops: List[HarvestCropCreate]  # <- LISTA DE CULTURAS PLANTADAS

class Harvest(HarvestBase):
    id: int

    class Config:
        from_attributes = True

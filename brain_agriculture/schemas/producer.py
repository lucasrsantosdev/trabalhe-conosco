from pydantic import BaseModel, Field
from typing import List, Optional


class HarvestCropCreate(BaseModel):
    crop_name: str
    harvest_year: int


class HarvestCreate(BaseModel):
    year: int
    crops: List[HarvestCropCreate]


class FarmCreateNested(BaseModel):
    name: str
    city: str
    state: str
    total_area: float
    arable_area: float
    vegetation_area: float
    harvests: List[HarvestCreate]


class ProducerFullCreate(BaseModel):
    document: str = Field(..., description="CPF ou CNPJ")
    name: str
    farm: FarmCreateNested

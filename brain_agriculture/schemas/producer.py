# brain_agriculture/schemas/producer.py
from datetime import date
from typing import List

from pydantic import BaseModel, Field, field_validator

from brain_agriculture.schemas.farm import FarmCreate
from brain_agriculture.validators.cpf_cnpj import validate_cpf_cnpj


# ====== INPUTS ======
class ProducerCreate(BaseModel):
    cpf_cnpj: str = Field(..., description="CPF ou CNPJ")
    name: str

    @field_validator("cpf_cnpj")
    @classmethod
    def _cpf_cnpj_ok(cls, v: str):
        if not validate_cpf_cnpj(v):
            raise ValueError("CPF/CNPJ inválido")
        return v


class ProducerFullCreate(ProducerCreate):
    farms: List[FarmCreate]

    class Config:
        from_attributes = True


# ====== OUTPUTS BÁSICOS ======
class Producer(BaseModel):
    id: int
    cpf_cnpj: str
    name: str

    class Config:
        from_attributes = True


# ====== OUTPUT ANINHADO (GET /producer-full) ======
class CropInfo(BaseModel):
    name: str


class HarvestInfo(BaseModel):
    name: str
    start_date: date
    end_date: date
    crops: List[CropInfo]


class FarmInfo(BaseModel):
    name: str
    city: str
    state: str
    area_total: float
    area_agricultavel: float
    area_vegetacao: float
    harvests: List[HarvestInfo]


class ProducerFullResponse(BaseModel):
    id: int
    cpf_cnpj: str
    name: str
    farms: List[FarmInfo]

    class Config:
        from_attributes = True

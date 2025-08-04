from pydantic import BaseModel, Field
from typing import List
from brain_agriculture.schemas.farm import FarmCreate

# Requisição base
class ProducerCreate(BaseModel):
    cpf_cnpj: str = Field(..., description="CPF ou CNPJ")
    name: str

# Requisição completa com fazendas
class ProducerFullCreate(ProducerCreate):
    farms: List[FarmCreate]

    class Config:
        from_attributes = True

# Resposta
class Producer(BaseModel):
    id: int
    cpf_cnpj: str
    name: str

    class Config:
        from_attributes = True

# brain_agriculture/schemas/farm.py

from pydantic import BaseModel, field_validator
from typing import Optional


class FarmBase(BaseModel):
    name: str
    city: str
    state: str
    area_total: float
    area_agricultavel: float
    area_vegetacao: float

    @field_validator("area_vegetacao", mode="after")
    @classmethod
    def validate_total_area(cls, v, values):
        area_agricultavel = values.get("area_agricultavel")
        area_total = values.get("area_total")

        if area_agricultavel is not None and area_total is not None:
            soma = area_agricultavel + v
            if soma > area_total:
                raise ValueError("A soma da área agricultável e vegetação não pode ser maior que a área total.")
        return v


class FarmCreate(FarmBase):
    pass


class Farm(FarmBase):
    id: int
    producer_id: Optional[int]  # O produtor a que essa fazenda pertence

    class Config:
        from_attributes = True


class FarmUpdate(FarmBase):
    pass

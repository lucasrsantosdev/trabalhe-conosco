# brain_agriculture/schemas/crop.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class CropBase(BaseModel):
    name: str


class CropCreate(CropBase):
    pass


class Crop(CropBase):
    id: UUID

    class Config:
        orm_mode = True

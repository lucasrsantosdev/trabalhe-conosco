# brain_agriculture/schemas/harvest_crop.py

from pydantic import BaseModel
from typing import Optional

class HarvestCropBase(BaseModel):
    harvest_id: int
    crop_id: int
    quantity: float

class HarvestCropCreate(HarvestCropBase):
    pass

class HarvestCrop(HarvestCropBase):
    id: int

    class Config:
        from_attributes = True

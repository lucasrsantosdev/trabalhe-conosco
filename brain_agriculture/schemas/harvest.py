# brain_agriculture/schemas/harvest.py

from pydantic import BaseModel
from datetime import date
from typing import Optional

class HarvestBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    farm_id: int

class HarvestCreate(HarvestBase):
    pass

class Harvest(HarvestBase):
    id: int

    class Config:
        from_attributes = True

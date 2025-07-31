# app/main.py

from fastapi import FastAPI
from app.core.database import engine
from app.models.base import Base

# 👇 IMPORTANTE: importa os modelos para registrá-los no Base.metadata
from app.models import producer, farm, crop, harvest, harvest_crop

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

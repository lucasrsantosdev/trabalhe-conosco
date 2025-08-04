# brain_agriculture/main.py
from fastapi import FastAPI

# Importa os models e base do SQLAlchemy
from brain_agriculture.models.base import Base
from brain_agriculture import database

# Importa as rotas definidas
from brain_agriculture.app.routes import (
    producer,
    farm,
    crop,
    harvest,
    harvest_crop,
)

# Cria as tabelas automaticamente no banco de dados ao iniciar a aplicação
Base.metadata.create_all(bind=database.engine)

# Cria a instância principal da aplicação FastAPI
app = FastAPI()

# Registra todas as rotas no app
app.include_router(producer.router)
app.include_router(farm.router)
app.include_router(crop.router)
app.include_router(harvest.router)
app.include_router(harvest_crop.router)

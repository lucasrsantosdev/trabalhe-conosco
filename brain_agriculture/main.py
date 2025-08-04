# brain_agriculture/main.py

from fastapi import FastAPI

# Importa os módulos internos
from brain_agriculture import database, models
from brain_agriculture.models.base import Base
from brain_agriculture.app.routes import producer, farm, crop

# Cria as tabelas no banco de dados automaticamente no startup
Base.metadata.create_all(bind=database.engine)

# Cria a instância principal da aplicação
app = FastAPI()

# Registra todas as rotas no app
app.include_router(producer.router)
app.include_router(farm.router)
app.include_router(crop.router)

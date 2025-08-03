# brain_agriculture/main.py

from fastapi import FastAPI
from brain_agriculture.database import engine
from brain_agriculture.models import base
from brain_agriculture.app.routes import producer

# Cria as tabelas automaticamente no startup
base.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inclui as rotas dos produtores
app.include_router(producer.router)

from fastapi import FastAPI
from brain_agriculture.app.routes import producer

app = FastAPI()

app.include_router(producer.router)

@app.get("/")
def read_root():
    return {"message": "API Brain Agriculture está rodando!"}

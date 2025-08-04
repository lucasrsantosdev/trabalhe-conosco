from pydantic import BaseModel

# Schema para leitura (GET /producers)
class Producer(BaseModel):
    id: int
    name: str
    document: str

    class Config:
        from_attributes = True  # Corrigido: indentação correta (equivalente ao antigo orm_mode = True)

# Schema para criação/atualização (POST/PUT /producers)
class ProducerCreate(BaseModel):
    name: str
    document: str

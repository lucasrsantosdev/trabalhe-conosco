# brain_agriculture/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# URL de conexão com o banco de dados SQLite local (para testes)
SQLALCHEMY_DATABASE_URL = "sqlite:///./brain_agriculture.db"

# Cria o engine de conexão
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria o gerenciador de sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM herdarem
Base = declarative_base()

# Função de dependência para usar nas rotas com FastAPI
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

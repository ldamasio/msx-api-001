from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi import Depends
from app.core.config import settings

# URL do banco de dados
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Criação do mecanismo de conexão com o banco de dados
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criação da fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para as classes de modelo
Base = declarative_base()

def get_db():
    """Função para obter uma sessão do banco de dados."""
    db = SessionLocal()  # Cria uma nova sessão
    try:
        yield db  # Retorna a sessão para uso
    finally:
        db.close()  # Fecha a sessão após o uso

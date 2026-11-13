"""
Configuração do banco de dados relacional com SQLAlchemy.
"""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import URL_BANCO_DADOS

# Engine para SQLite com verificação de thread desabilitada para FastAPI
engine = create_engine(
    URL_BANCO_DADOS,
    connect_args={"check_same_thread": False} if "sqlite" in URL_BANCO_DADOS else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def obter_banco_dados() -> Generator[Session, None, None]:
    """
    Injeção de dependência que fornece uma sessão do banco de dados e a fecha ao finalizar.
    """
    banco = SessionLocal()
    try:
        yield banco
    finally:
        banco.close()

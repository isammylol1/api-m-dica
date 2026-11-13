"""
Configuração global de fixtures de teste para o Pytest.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, obter_banco_dados
from app.main import app

# Configuração de engine SQLite compartilhado com StaticPool
engine_teste = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_teste)


@pytest.fixture(scope="session", autouse=True)
def setup_banco():
    Base.metadata.create_all(bind=engine_teste)
    yield
    Base.metadata.drop_all(bind=engine_teste)


def sobrescrever_obter_banco_dados():
    banco = TestingSessionLocal()
    try:
        yield banco
    finally:
        banco.close()


app.dependency_overrides[obter_banco_dados] = sobrescrever_obter_banco_dados


@pytest.fixture
def cliente():
    with TestClient(app) as c:
        yield c

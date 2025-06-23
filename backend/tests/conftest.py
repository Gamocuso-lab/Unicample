import pytest
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
import os

from app.main import app

# Banco de dados em memória para testes
TEST_DB_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    try:
        os.remove("./test.db")
    except:
        pass

@pytest.fixture(scope="function")
def db_session(test_engine):
    with Session(test_engine) as session:
        yield session
        session.rollback()

@pytest.fixture(scope="function")
def client(monkeypatch, db_session):
    # Substitui a dependência de sessão
    def get_test_session():
        yield db_session
    
    monkeypatch.setattr("app.db.session.get_session", get_test_session)
    
    # Retorna cliente de teste
    with TestClient(app) as c:
        yield c
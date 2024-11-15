import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.core.database import Base, get_db
from src.main import app

# Configuração do banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixture para criar o banco de dados de teste
@pytest.fixture(scope="function")
def db_session():
    # Criar as tabelas no banco de dados de teste
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Dropar as tabelas após o teste
        Base.metadata.drop_all(bind=engine)


# Fixture para o cliente da aplicação
@pytest.fixture(scope="function")
def client(db_session):
    # Sobrescrever a dependência get_db para usar a sessão de teste
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Limpar a sobrescrita após os testes
    app.dependency_overrides.clear()

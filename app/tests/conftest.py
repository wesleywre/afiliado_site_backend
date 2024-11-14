import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.core.database import Base, get_db
from src.core.security import create_access_token, get_password_hash
from src.main import app
from src.models.user import User  # Assegure-se de que o caminho está correto

# Configuração do banco de dados de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def test_db():
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    yield
    # Remove todas as tabelas
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client


@pytest.fixture
def normal_user_token_headers(client: TestClient, test_db: sessionmaker):
    """
    Fixture para gerar cabeçalhos de autorização para um usuário normal.
    """
    # Cria um usuário de teste
    user_email = "testuser@example.com"
    user_password = "testpassword"
    user_username = "testuserr"

    hashed_password = get_password_hash(user_password)
    user = User(
        email=user_email,
        username=user_username,  # Adicionado
        hashed_password=hashed_password,
        is_active=True,
        role="user",  # Ajuste conforme o seu modelo de papéis
    )

    # Adiciona o usuário ao banco de dados de teste
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)

    # Gera o token de acesso para o usuário
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    headers = {"Authorization": f"Bearer {access_token}"}

    db.close()

    return headers

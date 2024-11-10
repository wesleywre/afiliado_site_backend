# app/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.database import Base, get_db
from src.core.security import create_access_token, get_password_hash
from src.main import app
from src.models.user import User, UserRole

# Configuração do banco SQLite em memória
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Sobreescrever a dependência do banco de dados
async def override_get_db():
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    """Fixture para cliente de teste"""
    return TestClient(app)


@pytest.fixture(scope="function")
async def db():
    """Fixture para banco de dados de teste"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_user(db: AsyncSession):
    """Fixture para criar usuário normal"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("password123"),
        full_name="Test User",
        role=UserRole.USER,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def test_moderator(db: AsyncSession):
    """Fixture para criar moderador"""
    moderator = User(
        email="mod@example.com",
        username="moderator",
        hashed_password=get_password_hash("password123"),
        full_name="Test Moderator",
        role=UserRole.MODERATOR,
        is_active=True,
    )
    db.add(moderator)
    await db.commit()
    await db.refresh(moderator)
    return moderator


@pytest.fixture
def auth_headers(test_user):
    """Fixture para gerar headers de autenticação para usuário normal"""
    access_token = create_access_token(
        data={"sub": test_user.email, "role": test_user.role}
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def moderator_headers(test_moderator):
    """Fixture para gerar headers de autenticação para moderador"""
    access_token = create_access_token(
        data={"sub": test_moderator.email, "role": test_moderator.role}
    )
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def promotion_data():
    """Fixture com dados de exemplo para promoção"""
    return {
        "title": "Test Promotion",
        "description": "Test Description",
        "price": 99.99,
        "original_price": 199.99,
        "link": "https://example.com",
        "store": "Test Store",
        "category": "ELECTRONICS",
    }

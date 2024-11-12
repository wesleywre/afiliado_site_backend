from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import get_db, Base
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.crud.crud_user import create_user

client = TestClient(app)

def test_create_user(db: Session):
    user_in = UserCreate(email="test@example.com", password="password")
    user = create_user(db, user=user_in)
    assert user.email == "test@example.com"

def test_read_user(db: Session):
    user = db.query(User).filter(User.email == "test@example.com").first()
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
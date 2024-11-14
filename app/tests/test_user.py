# tests/test_user.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_password_hash
from src.main import app
from src.models.user import User

client = TestClient(app)


def test_create_user(db_session: Session):
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "full_name": "Novo Usuário",
        "password": "securepassword",
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data


def test_user_login(db_session: Session):
    login_data = {"username": "newuser@example.com", "password": "securepassword"}
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_read_users_me(db_session: Session):
    login_data = {"username": "newuser@example.com", "password": "securepassword"}
    login_response = client.post("/token", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"


def test_update_user_me(db_session: Session):
    login_data = {"username": "newuser@example.com", "password": "securepassword"}
    login_response = client.post("/token", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    update_data = {"full_name": "Usuário Atualizado"}
    response = client.put("/me", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Usuário Atualizado"


def test_delete_user_me(db_session: Session):
    login_data = {"username": "newuser@example.com", "password": "securepassword"}
    login_response = client.post("/token", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete("/users/me", headers=headers)
    assert response.status_code == 204

    response = client.get("/me", headers=headers)
    assert response.status_code == 401  # Não autorizado


def test_delete_user_by_admin(db_session: Session):
    # Criar usuário a ser deletado
    user = User(
        email="usertodelete@example.com",
        username="usertodelete",
        hashed_password=get_password_hash("password"),
        is_active=True,
        role=1,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Criar usuário admin
    admin_user = User(
        email="admin@example.com",
        username="adminuser",
        hashed_password=get_password_hash("adminpassword"),
        is_active=True,
        role=1,
    )
    db_session.add(admin_user)
    db_session.commit()
    db_session.refresh(admin_user)

    # Login como admin
    login_data = {"username": "admin@example.com", "password": "adminpassword"}
    login_response = client.post("/token", data=login_data)
    assert login_response.status_code == 200, login_response.text
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Deletar o usuário criado
    response = client.delete(f"/users/{user.id}", headers=headers)
    assert response.status_code == 204

    # Verificar se o usuário foi realmente deletado
    response = client.get(f"/users/{user.id}", headers=headers)
    assert response.status_code == 404

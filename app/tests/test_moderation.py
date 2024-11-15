# tests/test_moderation.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_password_hash
from src.main import app
from src.models.comment import Comment
from src.models.coupon import Coupon, CouponStatus
from src.models.promotion import Promotion, PromotionStatus
from src.models.user import User


@pytest.fixture
def regular_user(db_session: Session):
    user = User(
        email="user@example.com",
        username="user",
        hashed_password=get_password_hash("password"),
        is_active=True,
        role="USER",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def moderator_user(db_session: Session):
    user = User(
        email="moderator@example.com",
        username="moderator",
        hashed_password=get_password_hash("password"),
        is_active=True,
        role="MODERATOR",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_user(db_session: Session):
    user = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("password"),
        is_active=True,
        role="ADMIN",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def test_regular_user_cannot_access_moderation_routes(
    client: TestClient, db_session: Session, regular_user
):
    # Login como usuário comum
    login_data = {"username": regular_user.email, "password": "password"}
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Tentar acessar rota de moderação de promoções
    response = client.get("/moderation/promotions/pending", headers=headers)
    assert response.status_code == 403

    # Tentar acessar rota de moderação de cupons
    response = client.get("/moderation/coupons/pending", headers=headers)
    assert response.status_code == 403


def test_moderator_can_access_moderation_routes(
    client: TestClient, db_session: Session, moderator_user
):
    # Login como moderador
    login_data = {"username": moderator_user.email, "password": "password"}
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Acessar rota de moderação de promoções
    response = client.get("/moderation/promotions/pending", headers=headers)
    assert response.status_code == 200


def test_admin_can_access_moderation_routes(
    client: TestClient, db_session: Session, admin_user
):
    # Login como administrador
    login_data = {"username": admin_user.email, "password": "password"}
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Acessar rota de moderação de promoções
    response = client.get("/moderation/promotions/pending", headers=headers)
    assert response.status_code == 200


def test_moderator_can_approve_promotion(
    client: TestClient, db_session: Session, moderator_user
):
    # Criar promoção pendente
    promotion = Promotion(
        product="Produto Teste",
        link="http://example.com",
        comment="Descrição da promoção",
        price=157.20,
        status=PromotionStatus.PENDING,
        user_id=moderator_user.id,
    )
    db_session.add(promotion)
    db_session.commit()
    db_session.refresh(promotion)

    # Login como moderador
    login_data = {"username": moderator_user.email, "password": "password"}
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Aprovar a promoção
    # Aprovar a promoção
    update_data = {"status": "APPROVED"}
    response = client.put(
        f"/moderation/promotions/{promotion.id}", json=update_data, headers=headers
    )

    if response.status_code != 200:
        print(response.json())

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "APPROVED"


def test_moderator_can_delete_promotion(
    client: TestClient, db_session: Session, moderator_user
):
    # Criar promoção
    promotion = Promotion(
        product="Produto para Excluir",
        link="http://example.com",
        comment="Promoção a ser deletada",
        price=157.20,
        status=PromotionStatus.PENDING,
        user_id=moderator_user.id,
    )
    db_session.add(promotion)
    db_session.commit()
    db_session.refresh(promotion)

    # Login como moderador
    login_data = {"username": moderator_user.email, "password": "password"}
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Deletar a promoção
    response = client.delete(f"/moderation/promotions/{promotion.id}", headers=headers)
    assert response.status_code == 204

    # Verificar se a promoção foi deletada
    deleted_promotion = (
        db_session.query(Promotion).filter(Promotion.id == promotion.id).first()
    )
    assert deleted_promotion is None


def test_users_see_only_approved_promotions(
    client: TestClient, db_session: Session, regular_user
):
    # Criar promoções com diferentes status
    approved_promotion = Promotion(
        product="Promoção Aprovada",
        link="http://example.com",
        comment="Promoção aprovada",
        price=157.20,
        status=PromotionStatus.APPROVED,
        user_id=regular_user.id,
    )
    pending_promotion = Promotion(
        product="Promoção Pendente",
        link="http://example.com",
        comment="Promoção pendente",
        price=157.20,
        status=PromotionStatus.PENDING,
        user_id=regular_user.id,
    )
    db_session.add(approved_promotion)
    db_session.add(pending_promotion)
    db_session.commit()

    # Login como usuário
    login_data = {"username": regular_user.email, "password": "password"}
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Obter lista de promoções
    response = client.get("/promotions/", headers=headers)
    assert response.status_code == 200
    promotions = response.json()
    assert len(promotions) == 1
    assert promotions[0]["product"] == "Promoção Aprovada"

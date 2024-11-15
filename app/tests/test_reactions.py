import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_password_hash
from src.main import app
from src.models.comment import Comment
from src.models.coupon import Coupon, CouponStatus
from src.models.promotion import Promotion, PromotionStatus
from src.models.reaction import Reaction as ReactionModel
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


def test_user_can_like_promotion(client: TestClient, db_session: Session, regular_user):
    # Criar promoção aprovada
    promotion = Promotion(
        product="Produto para Curtir",
        link="http://example.com",
        comment="Descrição",
        price=157.42,
        status=PromotionStatus.APPROVED,
        user_id=regular_user.id,
    )
    db_session.add(promotion)
    db_session.commit()

    # Login como usuário
    login_data = {"username": regular_user.email, "password": "password"}
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Curtir a promoção
    reaction_data = {"promotion_id": promotion.id}
    response = client.post("/reactions/", json=reaction_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["promotion_id"] == promotion.id
    assert data["user_id"] == regular_user.id


def test_user_cannot_like_promotion_twice(
    client: TestClient, db_session: Session, regular_user
):
    promotion = Promotion(
        product="Produto para Curtir",
        link="http://example.com",
        comment="Descrição",
        price=157.42,
        status=PromotionStatus.APPROVED,
        user_id=regular_user.id,
    )
    db_session.add(promotion)
    db_session.commit()

    login_data = {"username": regular_user.email, "password": "password"}
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Tentar curtir novamente
    reaction_data = {"promotion_id": promotion.id}
    response = client.post("/reactions/", json=reaction_data, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Você já curtiu esta promoção."


def test_user_can_remove_reaction(
    client: TestClient, db_session: Session, regular_user
):
    promotion = Promotion(
        product="Produto para Curtir",
        link="http://example.com",
        comment="Descrição",
        price=157.42,
        status=PromotionStatus.APPROVED,
        user_id=regular_user.id,
    )
    db_session.add(promotion)
    db_session.commit()

    login_data = {"username": regular_user.email, "password": "password"}
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Remover reação
    params = {"promotion_id": promotion.id}
    response = client.delete("/reactions/", params=params, headers=headers)
    assert response.status_code == 204

    # Verificar se a reação foi removida
    reaction = (
        db_session.query(ReactionModel)
        .filter_by(user_id=regular_user.id, promotion_id=promotion.id)
        .first()
    )
    assert reaction is None

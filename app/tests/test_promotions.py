# app/tests/test_promotions.py
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.crud.promotion import PromotionCRUD
from src.models.promotion import Promotion, PromotionCategory, PromotionStatus


@pytest.fixture
def promotion_data():
    """Fixture com dados básicos de uma promoção"""
    return {
        "title": "Test Promotion",
        "description": "Test Description",
        "price": 99.99,
        "original_price": 199.99,
        "link": "https://example.com",
        "store": "Test Store",
        "category": PromotionCategory.ELECTRONICS,
    }


@pytest.fixture
async def test_promotion(db: Session, test_user, promotion_data):
    """Fixture que cria uma promoção no banco de teste"""
    return await PromotionCRUD.create(db, obj_in=promotion_data, user_id=test_user.id)


@pytest.mark.asyncio
async def test_create_promotion(
    client: TestClient, promotion_data: dict, auth_headers: dict
):
    """Testa a criação de uma promoção"""
    response = client.post(
        "/api/v1/promotions/", headers=auth_headers, json=promotion_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == promotion_data["title"]
    assert data["status"] == PromotionStatus.PENDING
    assert "id" in data


@pytest.mark.asyncio
async def test_get_promotion(client: TestClient, test_promotion: Promotion):
    """Testa a obtenção de uma promoção específica"""
    response = await client.get(f"/api/v1/promotions/{test_promotion.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_promotion.id
    assert data["title"] == test_promotion.title


@pytest.mark.asyncio
async def test_list_promotions(client: TestClient, test_promotion: Promotion):
    """Testa a listagem de promoções"""
    response = await client.get("/api/v1/promotions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_approve_promotion(
    client: TestClient, test_promotion: Promotion, moderator_headers: dict
):
    """Testa a aprovação de uma promoção por um moderador"""
    response = await client.put(
        f"/api/v1/promotions/{test_promotion.id}/approve", headers=moderator_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == PromotionStatus.APPROVED
    assert data["moderator_id"] is not None
    assert data["approved_at"] is not None


@pytest.mark.asyncio
async def test_reject_promotion(
    client: TestClient, test_promotion: Promotion, moderator_headers: dict
):
    """Testa a rejeição de uma promoção por um moderador"""
    response = await client.put(
        f"/api/v1/promotions/{test_promotion.id}/reject",
        headers=moderator_headers,
        json={"reason": "Test rejection"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == PromotionStatus.REJECTED
    assert data["rejection_reason"] == "Test rejection"


@pytest.mark.asyncio
async def test_increment_views(client: TestClient, test_promotion: Promotion):
    """Testa o incremento de visualizações"""
    initial_views = test_promotion.views_count
    response = await client.get(f"/api/v1/promotions/{test_promotion.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["views_count"] == initial_views + 1


@pytest.mark.asyncio
async def test_increment_clicks(client: TestClient, test_promotion: Promotion):
    """Testa o incremento de cliques"""
    initial_clicks = test_promotion.clicks_count
    response = await client.post(f"/api/v1/promotions/{test_promotion.id}/click")
    assert response.status_code == 200
    data = response.json()
    assert data["clicks_count"] == initial_clicks + 1


@pytest.mark.asyncio
async def test_feature_promotion(
    client: TestClient, test_promotion: Promotion, moderator_headers: dict
):
    """Testa a marcação de uma promoção como destaque"""
    response = await client.put(
        f"/api/v1/promotions/{test_promotion.id}/feature", headers=moderator_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_featured"] is True

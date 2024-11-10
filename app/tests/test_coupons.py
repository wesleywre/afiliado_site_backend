# app/tests/test_coupons.py
import pytest
from src.models.coupon import CouponStatus

from .conftest import test_moderator, test_user


@pytest.fixture
def coupon_data():
    return {
        "title": "Test Coupon",
        "code": "TEST123",
        "description": "Test Description",
        "link": "https://example.com",
        "store": "Test Store",
        "discount_value": "20% OFF",
    }


@pytest.fixture
def test_coupon(db, test_user, coupon_data):
    from src.crud.coupon import CouponCRUD

    return CouponCRUD.create(db, obj_in=coupon_data, user_id=test_user.id)


def test_create_coupon(client, coupon_data, auth_headers):
    response = client.post("/api/v1/coupons/", headers=auth_headers, json=coupon_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == coupon_data["code"].upper()
    assert data["status"] == CouponStatus.PENDING


def test_approve_coupon(client, test_coupon, moderator_headers):
    response = client.put(
        f"/api/v1/coupons/{test_coupon.id}/approve", headers=moderator_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == CouponStatus.APPROVED

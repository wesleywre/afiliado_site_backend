# src/routers/moderation_coupon.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_current_user
from src.models.coupon import Coupon as CouponModel
from src.models.user import User
from src.schemas.coupon import Coupon, CouponStatus, CouponUpdate

router = APIRouter()


def require_moderator(current_user: User = Depends(get_current_user)):
    if current_user.role not in ("ADMIN", "MODERATOR"):
        raise HTTPException(status_code=403, detail="Acesso negado")
    return current_user


@router.get("/pending", response_model=List[Coupon])
def get_pending_coupons(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator),
):
    coupons = (
        db.query(CouponModel)
        .filter(CouponModel.status == CouponStatus.PENDING)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return coupons


@router.put("/{coupon_id}", response_model=Coupon)
def update_coupon_status(
    coupon_id: int,
    coupon_in: CouponUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator),
):
    coupon = db.query(CouponModel).filter(CouponModel.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")

    update_data = coupon_in.dict(exclude_unset=True)
    if "link" in update_data:
        update_data["link"] = str(update_data["link"])  # Converter o link para string

    for var, value in update_data.items():
        setattr(coupon, var, value)

    db.commit()
    db.refresh(coupon)
    return coupon


@router.delete("/{coupon_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coupon(
    coupon_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator),
):
    coupon = db.query(CouponModel).filter(CouponModel.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")

    db.delete(coupon)
    db.commit()
    return None

# src/routers/coupon.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_current_user
from src.models.coupon import Coupon as CouponModel
from src.models.user import User
from src.schemas.coupon import Coupon, CouponCreate, CouponStatus, CouponUpdate

router = APIRouter()


@router.post("/", response_model=Coupon)
def create_coupon(
    coupon_in: CouponCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    coupon_data = coupon_in.dict()
    coupon_data["link"] = str(coupon_data["link"])  # Converter o link para string
    coupon = CouponModel(**coupon_data, user_id=current_user.id)
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon


@router.get("/", response_model=List[Coupon])
def read_coupons(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    coupons = (
        db.query(CouponModel)
        .filter(CouponModel.status == CouponStatus.APPROVED)
        .order_by(CouponModel.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return coupons


@router.get("/{coupon_id}", response_model=Coupon)
def read_coupon(coupon_id: int, db: Session = Depends(get_db)):
    coupon = (
        db.query(CouponModel)
        .filter(
            CouponModel.id == coupon_id,
            CouponModel.status == CouponStatus.APPROVED,
        )
        .first()
    )
    if not coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return coupon


@router.get("/pending/", response_model=List[Coupon])
def read_pending_coupons(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role not in ("MODERATOR", "ADMIN"):
        raise HTTPException(status_code=403, detail="Acesso negado")
    coupons = (
        db.query(CouponModel)
        .filter(CouponModel.status == CouponStatus.PENDING)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return coupons


@router.put("/{coupon_id}", response_model=Coupon)
def update_coupon(
    coupon_id: int,
    coupon_in: CouponUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    coupon = db.query(CouponModel).filter(CouponModel.id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    if coupon.user_id != current_user.id and current_user.role not in (
        "MODERATOR",
        "ADMIN",
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")

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
    current_user: User = Depends(get_current_user),
):
    coupon = db.query(CouponModel).filter(CouponModel.id == coupon_id).first()  # noqa :E501
    if not coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    if coupon.user_id != current_user.id and current_user.role not in (
        "MODERATOR",
        "ADMIN",
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")

    db.delete(coupon)
    db.commit()
    return None


@router.get("/search/")
async def search_coupons(
    q: str = Query(None), skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    query = db.query(CouponModel).filter(CouponModel.status == CouponStatus.APPROVED)

    if q:
        search = f"%{q}%"
        query = query.filter(
            or_(
                CouponModel.product.ilike(search),
                CouponModel.store.ilike(search),
                CouponModel.comment.ilike(search),
            )
        )

    coupons = query.order_by(CouponModel.created_at.desc()).offset(skip).limit(limit).all()
    return coupons

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.crud_coupon import get_coupon_by_id, get_coupons, create_coupon, update_coupon, delete_coupon
from app.schemas.coupon import CouponCreate, CouponUpdate, CouponOut
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=CouponOut)
def create_new_coupon(coupon: CouponCreate, db: Session = Depends(get_db)):
    return create_coupon(db=db, coupon=coupon)

@router.get("/{coupon_id}", response_model=CouponOut)
def read_coupon(coupon_id: int, db: Session = Depends(get_db)):
    db_coupon = get_coupon_by_id(db, coupon_id=coupon_id)
    if db_coupon is None:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return db_coupon

@router.get("/", response_model=List[CouponOut])
def read_coupons(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    coupons = get_coupons(db, skip=skip, limit=limit)
    return coupons

@router.put("/{coupon_id}", response_model=CouponOut)
def update_existing_coupon(coupon_id: int, coupon: CouponUpdate, db: Session = Depends(get_db)):
    return update_coupon(db=db, coupon_id=coupon_id, coupon=coupon)

@router.delete("/{coupon_id}", response_model=CouponOut)
def delete_existing_coupon(coupon_id: int, db: Session = Depends(get_db)):
    return delete_coupon(db=db, coupon_id=coupon_id)
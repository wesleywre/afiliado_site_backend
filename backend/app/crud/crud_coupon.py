from sqlalchemy.orm import Session
from app.models.coupon import Coupon
from app.schemas.coupon import CouponCreate, CouponUpdate

def get_coupon_by_id(db: Session, coupon_id: int):
    return db.query(Coupon).filter(Coupon.id == coupon_id).first()

def get_coupons(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Coupon).offset(skip).limit(limit).all()

def create_coupon(db: Session, coupon: CouponCreate):
    db_coupon = Coupon(
        title=coupon.title,
        link=coupon.link,
        code=coupon.code,
        user_id=coupon.user_id,
    )
    db.add(db_coupon)
    db.commit()
    db.refresh(db_coupon)
    return db_coupon

def update_coupon(db: Session, coupon_id: int, coupon: CouponUpdate):
    db_coupon = get_coupon_by_id(db, coupon_id)
    if db_coupon:
        for key, value in coupon.dict(exclude_unset=True).items():
            setattr(db_coupon, key, value)
        db.commit()
        db.refresh(db_coupon)
    return db_coupon

def delete_coupon(db: Session, coupon_id: int):
    db_coupon = get_coupon_by_id(db, coupon_id)
    if db_coupon:
        db.delete(db_coupon)
        db.commit()
    return db_coupon
from sqlalchemy.orm import Session
from app.models.like import Like
from app.schemas.like import LikeCreate, LikeUpdate

def get_like_by_id(db: Session, like_id: int):
    return db.query(Like).filter(Like.id == like_id).first()

def get_likes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Like).offset(skip).limit(limit).all()

def create_like(db: Session, like: LikeCreate):
    db_like = Like(
        user_id=like.user_id,
        promotion_id=like.promotion_id,
        coupon_id=like.coupon_id,
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

def update_like(db: Session, like_id: int, like: LikeUpdate):
    db_like = get_like_by_id(db, like_id)
    if db_like:
        for key, value in like.dict(exclude_unset=True).items():
            setattr(db_like, key, value)
        db.commit()
        db.refresh(db_like)
    return db_like

def delete_like(db: Session, like_id: int):
    db_like = get_like_by_id(db, like_id)
    if db_like:
        db.delete(db_like)
        db.commit()
    return db_like
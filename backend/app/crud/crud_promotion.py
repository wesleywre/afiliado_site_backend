from sqlalchemy.orm import Session
from app.models.promotion import Promotion
from app.schemas.promotion import PromotionCreate, PromotionUpdate

def get_promotion_by_id(db: Session, promotion_id: int):
    return db.query(Promotion).filter(Promotion.id == promotion_id).first()

def get_promotions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Promotion).offset(skip).limit(limit).all()

def create_promotion(db: Session, promotion: PromotionCreate):
    db_promotion = Promotion(
        title=promotion.title,
        link=promotion.link,
        price=promotion.price,
        user_id=promotion.user_id,
    )
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion

def update_promotion(db: Session, promotion_id: int, promotion: PromotionUpdate):
    db_promotion = get_promotion_by_id(db, promotion_id)
    if db_promotion:
        for key, value in promotion.dict(exclude_unset=True).items():
            setattr(db_promotion, key, value)
        db.commit()
        db.refresh(db_promotion)
    return db_promotion

def delete_promotion(db: Session, promotion_id: int):
    db_promotion = get_promotion_by_id(db, promotion_id)
    if db_promotion:
        db.delete(db_promotion)
        db.commit()
    return db_promotion
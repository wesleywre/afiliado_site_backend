from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.crud_promotion import get_promotion_by_id, get_promotions, create_promotion, update_promotion, delete_promotion
from app.schemas.promotion import PromotionCreate, PromotionUpdate, PromotionOut
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=PromotionOut)
def create_new_promotion(promotion: PromotionCreate, db: Session = Depends(get_db)):
    return create_promotion(db=db, promotion=promotion)

@router.get("/{promotion_id}", response_model=PromotionOut)
def read_promotion(promotion_id: int, db: Session = Depends(get_db)):
    db_promotion = get_promotion_by_id(db, promotion_id=promotion_id)
    if db_promotion is None:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return db_promotion

@router.get("/", response_model=List[PromotionOut])
def read_promotions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    promotions = get_promotions(db, skip=skip, limit=limit)
    return promotions

@router.put("/{promotion_id}", response_model=PromotionOut)
def update_existing_promotion(promotion_id: int, promotion: PromotionUpdate, db: Session = Depends(get_db)):
    return update_promotion(db=db, promotion_id=promotion_id, promotion=promotion)

@router.delete("/{promotion_id}", response_model=PromotionOut)
def delete_existing_promotion(promotion_id: int, db: Session = Depends(get_db)):
    return delete_promotion(db=db, promotion_id=promotion_id)
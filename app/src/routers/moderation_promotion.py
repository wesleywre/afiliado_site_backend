# src/routers/moderation_promotion.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_current_user
from src.models.promotion import Promotion as PromotionModel
from src.models.user import User
from src.schemas.promotion import Promotion, PromotionStatus, PromotionUpdate

router = APIRouter()


def require_moderator(current_user: User = Depends(get_current_user)):
    if current_user.role not in ("ADMIN", "MODERATOR"):
        raise HTTPException(status_code=403, detail="Acesso negado")
    return current_user


@router.get("/pending", response_model=List[Promotion])
def get_pending_promotions(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator),
):
    promotions = (
        db.query(PromotionModel)
        .filter(PromotionModel.status == PromotionStatus.PENDING)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return promotions


@router.put("/{promotion_id}", response_model=Promotion)
def update_promotion_status(
    promotion_id: int,
    promotion_in: PromotionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator),
):
    promotion = (
        db.query(PromotionModel).filter(PromotionModel.id == promotion_id).first()
    )
    if not promotion:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")

    update_data = promotion_in.dict(exclude_unset=True)
    if "link" in update_data:
        update_data["link"] = str(update_data["link"])  # Converter o link para string

    for var, value in update_data.items():
        setattr(promotion, var, value)

    db.commit()
    db.refresh(promotion)
    return promotion


@router.delete("/{promotion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator),
):
    promotion = (
        db.query(PromotionModel).filter(PromotionModel.id == promotion_id).first()
    )
    if not promotion:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")

    db.delete(promotion)
    db.commit()
    return None

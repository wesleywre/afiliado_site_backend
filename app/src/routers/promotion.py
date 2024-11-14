from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_current_user
from src.models.promotion import Promotion as PromotionModel
from src.models.user import User
from src.schemas.promotion import (
    Promotion,
    PromotionCreate,
    PromotionStatus,
    PromotionUpdate,
)

router = APIRouter()


@router.post("/", response_model=Promotion)
def create_promotion(
    promotion_in: PromotionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    promotion_data = promotion_in.dict()
    promotion_data["link"] = str(promotion_data["link"])  # Converter o link para string
    promotion = PromotionModel(**promotion_data, user_id=current_user.id)
    db.add(promotion)
    db.commit()
    db.refresh(promotion)
    return promotion


@router.get("/", response_model=List[Promotion])
def read_promotions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    promotions = (
        db.query(PromotionModel)
        .filter(PromotionModel.status == PromotionStatus.APPROVED)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return promotions


@router.get("/{promotion_id}", response_model=Promotion)
def read_promotion(promotion_id: int, db: Session = Depends(get_db)):
    promotion = (
        db.query(PromotionModel)
        .filter(
            PromotionModel.id == promotion_id,
            PromotionModel.status == PromotionStatus.APPROVED,
        )
        .first()
    )
    if not promotion:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")
    return promotion


@router.get("/pending/", response_model=List[Promotion])
def read_pending_promotions(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role not in ("MODERATOR", "ADMIN"):
        raise HTTPException(status_code=403, detail="Acesso negado")
    promotions = (
        db.query(PromotionModel)
        .filter(PromotionModel.status == PromotionStatus.PENDING)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return promotions


@router.put("/{promotion_id}", response_model=Promotion)
def update_promotion(
    promotion_id: int,
    promotion_in: PromotionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    promotion = db.query(PromotionModel).filter(PromotionModel.id == promotion_id).first()
    if not promotion:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")
    if promotion.user_id != current_user.id and current_user.role not in (
        "MODERATOR",
        "ADMIN",
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")

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
    current_user: User = Depends(get_current_user),
):
    promotion = db.query(PromotionModel).filter(PromotionModel.id == promotion_id).first()
    if not promotion:
        raise HTTPException(status_code=404, detail="Promoção não encontrada")
    if promotion.user_id != current_user.id and current_user.role not in (
        "MODERATOR",
        "ADMIN",
    ):
        raise HTTPException(status_code=403, detail="Acesso negado")

    db.delete(promotion)
    db.commit()
    return None

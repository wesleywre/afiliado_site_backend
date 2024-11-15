# src/routers/reaction.py

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_current_user
from src.models.coupon import Coupon as CouponModel
from src.models.promotion import Promotion as PromotionModel
from src.models.reaction import Reaction as ReactionModel
from src.models.user import User as UserModel
from src.schemas.reaction import Reaction, ReactionCreate

router = APIRouter()


@router.post("/", response_model=Reaction)
def create_reaction(
    reaction_in: ReactionCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Verificar se um dos IDs foi fornecido
    if not reaction_in.promotion_id and not reaction_in.coupon_id:
        raise HTTPException(
            status_code=400,
            detail="É necessário especificar 'promotion_id' ou 'coupon_id'.",
        )
    # Verificar se apenas um dos IDs foi fornecido
    if reaction_in.promotion_id and reaction_in.coupon_id:
        raise HTTPException(
            status_code=400,
            detail="Não é possível reagir a uma promoção e a um cupom ao mesmo tempo.",
        )
    # Verificar se a promoção existe
    if reaction_in.promotion_id:
        promotion = (
            db.query(PromotionModel)
            .filter(PromotionModel.id == reaction_in.promotion_id)
            .first()
        )
        if not promotion:
            raise HTTPException(status_code=404, detail="Promoção não encontrada.")
        # Verificar se já existe uma reação do usuário nessa promoção
        existing_reaction = (
            db.query(ReactionModel)
            .filter(
                ReactionModel.user_id == current_user.id,
                ReactionModel.promotion_id == reaction_in.promotion_id,
            )
            .first()
        )
        if existing_reaction:
            raise HTTPException(status_code=400, detail="Você já curtiu esta promoção.")
    # Verificar se o cupom existe
    if reaction_in.coupon_id:
        coupon = (
            db.query(CouponModel)
            .filter(CouponModel.id == reaction_in.coupon_id)
            .first()
        )
        if not coupon:
            raise HTTPException(status_code=404, detail="Cupom não encontrado.")
        # Verificar se já existe uma reação do usuário nesse cupom
        existing_reaction = (
            db.query(ReactionModel)
            .filter(
                ReactionModel.user_id == current_user.id,
                ReactionModel.coupon_id == reaction_in.coupon_id,
            )
            .first()
        )
        if existing_reaction:
            raise HTTPException(status_code=400, detail="Você já curtiu este cupom.")

    reaction = ReactionModel(**reaction_in.model_dump(), user_id=current_user.id)
    db.add(reaction)
    db.commit()
    db.refresh(reaction)
    return reaction


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_reaction(
    promotion_id: Optional[int] = None,
    coupon_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Verificar se um dos IDs foi fornecido
    if not promotion_id and not coupon_id:
        raise HTTPException(
            status_code=400,
            detail="É necessário especificar 'promotion_id' ou 'coupon_id'.",
        )
    # Verificar se apenas um dos IDs foi fornecido
    if promotion_id and coupon_id:
        raise HTTPException(
            status_code=400,
            detail="Não é possível especificar ambos 'promotion_id' e 'coupon_id'.",
        )
    # Buscar a reação
    if promotion_id:
        reaction = (
            db.query(ReactionModel)
            .filter(
                ReactionModel.user_id == current_user.id,
                ReactionModel.promotion_id == promotion_id,
            )
            .first()
        )
    if coupon_id:
        reaction = (
            db.query(ReactionModel)
            .filter(
                ReactionModel.user_id == current_user.id,
                ReactionModel.coupon_id == coupon_id,
            )
            .first()
        )
    if not reaction:
        raise HTTPException(status_code=404, detail="Reação não encontrada.")

    db.delete(reaction)
    db.commit()
    return None


@router.get("/count", response_model=int)
def get_reactions_count(
    promotion_id: Optional[int] = None,
    coupon_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    # Verificar se um dos IDs foi fornecido
    if not promotion_id and not coupon_id:
        raise HTTPException(
            status_code=400,
            detail="É necessário especificar 'promotion_id' ou 'coupon_id'.",
        )
    if promotion_id and coupon_id:
        raise HTTPException(
            status_code=400,
            detail="Não é possível especificar ambos 'promotion_id' e 'coupon_id'.",
        )
    if promotion_id:
        count = (
            db.query(ReactionModel)
            .filter(ReactionModel.promotion_id == promotion_id)
            .count()
        )
    if coupon_id:
        count = (
            db.query(ReactionModel).filter(ReactionModel.coupon_id == coupon_id).count()
        )
    return count

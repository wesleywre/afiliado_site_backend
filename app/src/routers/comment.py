# src/routers/comment.py

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_current_user
from src.models.comment import Comment as CommentModel
from src.models.coupon import Coupon as CouponModel
from src.models.promotion import Promotion as PromotionModel
from src.models.user import User as UserModel
from src.schemas.comment import Comment as CommentSchema
from src.schemas.comment import CommentCreate, CommentUpdate

router = APIRouter()


@router.post("/", response_model=CommentSchema)
def create_comment(
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    # Verificar se um dos IDs foi fornecido
    if not comment_in.promotion_id and not comment_in.coupon_id:
        raise HTTPException(
            status_code=400,
            detail="É necessário especificar 'promotion_id' ou 'coupon_id'.",
        )
    # Verificar se apenas um dos IDs foi fornecido
    if comment_in.promotion_id and comment_in.coupon_id:
        raise HTTPException(
            status_code=400,
            detail="Não é possível comentar em promoção e cupom ao mesmo tempo.",
        )
    # Verificar se a promoção existe
    if comment_in.promotion_id:
        promotion = (
            db.query(PromotionModel).filter(PromotionModel.id == comment_in.promotion_id).first()
        )
        if not promotion:
            raise HTTPException(status_code=404, detail="Promoção não encontrada.")
    # Verificar se o cupom existe
    if comment_in.coupon_id:
        coupon = db.query(CouponModel).filter(CouponModel.id == comment_in.coupon_id).first()
        if not coupon:
            raise HTTPException(status_code=404, detail="Cupom não encontrado.")

    comment = CommentModel(**comment_in.model_dump(), user_id=current_user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/", response_model=List[CommentSchema])
def read_comments(
    promotion_id: Optional[int] = None,
    coupon_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    query = db.query(CommentModel)
    if promotion_id:
        query = query.filter(CommentModel.promotion_id == promotion_id)
    if coupon_id:
        query = query.filter(CommentModel.coupon_id == coupon_id)
    comments = query.order_by(CommentModel.created_at.asc()).offset(skip).limit(limit).all()

    return comments


@router.put("/{comment_id}", response_model=CommentSchema)
def update_comment(
    comment_id: int,
    comment_in: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comentário não encontrado.")

    # Verificar permissões: usuário pode atualizar apenas seu próprio comentário
    if comment.user_id != current_user.id and current_user.role not in (
        "ADMIN",
        "MODERATOR",
    ):
        raise HTTPException(status_code=403, detail="Não autorizado a editar este comentário.")

    update_data = comment_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(comment, key, value)
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comentário não encontrado.")

    # Apenas moderadores e administradores podem deletar comentários
    if current_user.role not in ("ADMIN", "MODERATOR"):
        raise HTTPException(status_code=403, detail="Não autorizado a deletar este comentário.")

    db.delete(comment)
    db.commit()
    return None

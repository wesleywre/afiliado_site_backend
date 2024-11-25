# src/routers/comment.py

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
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
    if not comment_in.promotion_id and not comment_in.coupon_id and not comment_in.parent_id:
        raise HTTPException(
            status_code=400,
            detail="É necessário especificar 'promotion_id', 'coupon_id' ou 'parent_id'.",
        )
    # Verificar se apenas um dos IDs foi fornecido (permitindo parent_id)
    related_fields = [comment_in.promotion_id, comment_in.coupon_id, comment_in.parent_id]
    provided_fields = [field for field in related_fields if field is not None]
    if len(provided_fields) != 1:
        raise HTTPException(
            status_code=400,
            detail="Especifique apenas um entre 'promotion_id', 'coupon_id' ou 'parent_id'.",
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
    # Verificar se o comentário pai existe
    if comment_in.parent_id:
        parent_comment = (
            db.query(CommentModel).filter(CommentModel.id == comment_in.parent_id).first()
        )
        if not parent_comment:
            raise HTTPException(status_code=404, detail="Comentário pai não encontrado.")

    comment = CommentModel(**comment_in.model_dump(), user_id=current_user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/", response_model=List[CommentSchema])
def read_comments(
    promotion_id: Optional[int] = None,
    coupon_id: Optional[int] = None,
    parent_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    query = db.query(CommentModel).options(joinedload(CommentModel.replies))
    if promotion_id:
        query = query.filter(CommentModel.promotion_id == promotion_id)
    if coupon_id:
        query = query.filter(CommentModel.coupon_id == coupon_id)
    if parent_id is not None:
        query = query.filter(CommentModel.parent_id == parent_id)
    else:
        # Se parent_id não for fornecido, filtramos por comentários de nível superior
        query = query.filter(CommentModel.parent_id.is_(None))

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

    # usuário pode deletar apenas seu próprio comentário ou ser moderador/admin
    if comment.user_id != current_user.id and current_user.role not in ("ADMIN", "MODERATOR"):
        raise HTTPException(status_code=403, detail="Não autorizado a deletar este comentário.")

    db.delete(comment)
    db.commit()
    return None


@router.get("/{comment_id}", response_model=CommentSchema)
def read_comment(
    comment_id: int,
    db: Session = Depends(get_db),
):
    comment = (
        db.query(CommentModel)
        .options(joinedload(CommentModel.replies))
        .filter(CommentModel.id == comment_id)
        .first()
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Comentário não encontrado.")

    return comment

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_current_user
from src.models.comment import Comment
from src.models.comment_like import CommentLike as CommentLikeModel
from src.models.user import User
from src.schemas.comment_like import CommentLike as CommentLikeSchema
from src.schemas.comment_like import CommentLikeCreate

router = APIRouter()


@router.post("/", response_model=CommentLikeSchema)
def like_comment(
    like_in: CommentLikeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.query(Comment).filter(Comment.id == like_in.comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    existing_like = (
        db.query(CommentLikeModel)
        .filter(
            CommentLikeModel.user_id == current_user.id,
            CommentLikeModel.comment_id == like_in.comment_id,
        )
        .first()
    )
    if existing_like:
        raise HTTPException(status_code=400, detail="Você já curtiu este comentário")

    like = CommentLikeModel(
        user_id=current_user.id,
        comment_id=like_in.comment_id,
    )
    db.add(like)
    db.commit()
    db.refresh(like)
    return like


@router.delete("/{comment_id}")
def unlike_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    like = (
        db.query(CommentLikeModel)
        .filter(
            CommentLikeModel.user_id == current_user.id, CommentLikeModel.comment_id == comment_id
        )
        .first()
    )
    if not like:
        raise HTTPException(status_code=404, detail="Curtida não encontrada")
    db.delete(like)
    db.commit()
    return {"detail": "Curtida removida com sucesso"}


@router.get("/count", response_model=int)
def get_reactions_count_comment(
    comment_id: int,
    db: Session = Depends(get_db),
):
    # Verificar se um dos IDs foi fornecido
    if not comment_id:
        raise HTTPException(
            status_code=400,
            detail="É necessário especificar comment_id.",
        )
    if comment_id:
        count = (
            db.query(CommentLikeModel).filter(CommentLikeModel.comment_id == comment_id).count()
        )
    return count


@router.get("/check", response_model=bool)
def check_user_reaction_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if comment_id is None:
        raise HTTPException(
            status_code=400,
            detail="Por favor, especifique 'comment_id'",
        )
    query = db.query(CommentLikeModel).filter(CommentLikeModel.user_id == user.id)
    if comment_id:
        query = query.filter(CommentLikeModel.comment_id == comment_id)
    return query.first() is not None

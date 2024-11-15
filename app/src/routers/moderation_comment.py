# src/routers/moderation_comment.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_current_user
from src.models.comment import Comment as CommentModel
from src.models.user import User
from src.schemas.comment import Comment, CommentUpdate

router = APIRouter()


def require_moderator(current_user: User = Depends(get_current_user)):
    if current_user.role not in ("ADMIN", "MODERATOR"):
        raise HTTPException(status_code=403, detail="Acesso negado")
    return current_user


@router.get("/", response_model=List[Comment])
def get_all_comments(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator),
):
    comments = db.query(CommentModel).offset(skip).limit(limit).all()
    return comments


@router.put("/{comment_id}", response_model=Comment)
def update_comment(
    comment_id: int,
    comment_in: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_moderator),
):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

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
    current_user: User = Depends(require_moderator),
):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    db.delete(comment)
    db.commit()
    return None

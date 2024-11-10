# app/src/crud/comment.py
from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.comment import Comment
from ..schemas.comment import CommentCreate, CommentUpdate
from .base import CRUDBase


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    async def get_by_promotion(
        self, db: Session, *, promotion_id: int, skip: int = 0, limit: int = 100
    ) -> List[Comment]:
        """Retorna comentários de uma promoção específica"""
        return (
            db.query(self.model)
            .filter(
                self.model.promotion_id == promotion_id,
                self.model.is_active == True,  # noqa :E712
            )
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def update_comment(
        self,
        db: Session,
        *,
        db_obj: Comment,
        obj_in: CommentUpdate,
        is_moderator: bool = False
    ) -> Comment:
        """
        Atualiza um comentário com verificações específicas
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if update_data.get("text"):
            setattr(db_obj, "is_edited", True)

        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def moderate_comment(
        self, db: Session, *, comment_id: int, is_active: bool, moderator_id: int
    ) -> Optional[Comment]:
        """
        Moderação de comentário
        """
        comment = await self.get(db, id=comment_id)
        if comment:
            setattr(comment, "is_active", is_active)
            db.add(comment)
            await db.commit()
            await db.refresh(comment)
        return comment


CommentCRUD = CRUDComment(Comment)

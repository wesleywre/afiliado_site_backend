from sqlalchemy.orm import Session

from ..models.like import PromotionLike
from ..schemas.like import PromotionLikeCreate
from .base import CRUDBase


class CRUDLike(CRUDBase[PromotionLike, PromotionLikeCreate, PromotionLikeCreate]):
    async def toggle_like(
        self, db: Session, *, user_id: int, promotion_id: int
    ) -> bool:
        """Toggle like status. Returns True if liked, False if unliked"""
        like = (
            db.query(self.model)
            .filter(
                self.model.user_id == user_id, self.model.promotion_id == promotion_id
            )
            .first()
        )

        if like:
            db.delete(like)
            await db.commit()
            return False

        db_obj = self.model(user_id=user_id, promotion_id=promotion_id)
        db.add(db_obj)
        await db.commit()
        return True


LikeCRUD = CRUDLike(PromotionLike)

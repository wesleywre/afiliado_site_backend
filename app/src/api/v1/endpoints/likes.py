from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import get_current_active_user
from ....crud.like import LikeCRUD
from ....models.user import User

router = APIRouter()


@router.post("/promotions/{promotion_id}/like")
async def toggle_like(
    promotion_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Toggle like em uma promoção"""
    is_liked = await LikeCRUD.toggle_like(
        db, user_id=current_user.id, promotion_id=promotion_id
    )
    return {"status": "liked" if is_liked else "unliked"}

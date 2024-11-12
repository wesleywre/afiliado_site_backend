from app.models.user import User
from sqlalchemy.orm import Session


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

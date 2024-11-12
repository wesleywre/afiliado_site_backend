from sqlalchemy.orm import Session
from app.models.view import View
from app.schemas.view import ViewCreate, ViewUpdate

def get_view_by_id(db: Session, view_id: int):
    return db.query(View).filter(View.id == view_id).first()

def get_views(db: Session, skip: int = 0, limit: int = 10):
    return db.query(View).offset(skip).limit(limit).all()

def create_view(db: Session, view: ViewCreate):
    db_view = View(
        promotion_id=view.promotion_id,
        coupon_id=view.coupon_id,
        view_count=view.view_count,
    )
    db.add(db_view)
    db.commit()
    db.refresh(db_view)
    return db_view

def update_view(db: Session, view_id: int, view: ViewUpdate):
    db_view = get_view_by_id(db, view_id)
    if db_view:
        for key, value in view.dict(exclude_unset=True).items():
            setattr(db_view, key, value)
        db.commit()
        db.refresh(db_view)
    return db_view

def delete_view(db: Session, view_id: int):
    db_view = get_view_by_id(db, view_id)
    if db_view:
        db.delete(db_view)
        db.commit()
    return db_view
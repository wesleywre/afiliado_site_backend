from app.models.permission import Permission
from app.schemas.permission import PermissionCreate
from sqlalchemy.orm import Session


def create_permission(db: Session, permission: PermissionCreate):
    db_permission = Permission(name=permission.name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def get_permissions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Permission).offset(skip).limit(limit).all()

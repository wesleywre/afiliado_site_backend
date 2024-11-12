from typing import List

from app.crud.crud_permission import create_permission, get_permissions
from app.database import get_db
from app.schemas.permission import PermissionOut, PermissionCreate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/permissions/", response_model=PermissionOut)
def create_new_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    return create_permission(db=db, permission=permission)


@router.get("/permissions/", response_model=List[PermissionOut])
def read_permissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    permissions = get_permissions(db, skip=skip, limit=limit)
    return permissions

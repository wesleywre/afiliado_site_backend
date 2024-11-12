from typing import List

from app.crud.crud_role import create_role, get_roles
from app.database import get_db
from app.schemas.role import Role, RoleCreate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/roles/", response_model=Role)
def create_new_role(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db=db, role=role)


@router.get("/roles/", response_model=List[Role])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    roles = get_roles(db, skip=skip, limit=limit)
    return roles

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.crud_view import get_view_by_id, get_views, create_view, update_view, delete_view
from app.schemas.view import ViewCreate, ViewUpdate, ViewOut
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=ViewOut)
def create_new_view(view: ViewCreate, db: Session = Depends(get_db)):
    return create_view(db=db, view=view)

@router.get("/{view_id}", response_model=ViewOut)
def read_view(view_id: int, db: Session = Depends(get_db)):
    db_view = get_view_by_id(db, view_id=view_id)
    if db_view is None:
        raise HTTPException(status_code=404, detail="View not found")
    return db_view

@router.get("/", response_model=List[ViewOut])
def read_views(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    views = get_views(db, skip=skip, limit=limit)
    return views

@router.put("/{view_id}", response_model=ViewOut)
def update_existing_view(view_id: int, view: ViewUpdate, db: Session = Depends(get_db)):
    return update_view(db=db, view_id=view_id, view=view)

@router.delete("/{view_id}", response_model=ViewOut)
def delete_existing_view(view_id: int, db: Session = Depends(get_db)):
    return delete_view(db=db, view_id=view_id)
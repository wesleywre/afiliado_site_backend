from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.crud_like import get_like_by_id, get_likes, create_like, update_like, delete_like
from app.schemas.like import LikeCreate, LikeUpdate, LikeOut
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=LikeOut)
def create_new_like(like: LikeCreate, db: Session = Depends(get_db)):
    return create_like(db=db, like=like)

@router.get("/{like_id}", response_model=LikeOut)
def read_like(like_id: int, db: Session = Depends(get_db)):
    db_like = get_like_by_id(db, like_id=like_id)
    if db_like is None:
        raise HTTPException(status_code=404, detail="Like not found")
    return db_like

@router.get("/", response_model=List[LikeOut])
def read_likes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    likes = get_likes(db, skip=skip, limit=limit)
    return likes

@router.put("/{like_id}", response_model=LikeOut)
def update_existing_like(like_id: int, like: LikeUpdate, db: Session = Depends(get_db)):
    return update_like(db=db, like_id=like_id, like=like)

@router.delete("/{like_id}", response_model=LikeOut)
def delete_existing_like(like_id: int, db: Session = Depends(get_db)):
    return delete_like(db=db, like_id=like_id)
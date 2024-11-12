from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud.crud_comment import get_comment_by_id, get_comments, create_comment, update_comment, delete_comment
from app.schemas.comment import CommentCreate, CommentUpdate, CommentOut
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=CommentOut)
def create_new_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    return create_comment(db=db, comment=comment)

@router.get("/{comment_id}", response_model=CommentOut)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = get_comment_by_id(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.get("/", response_model=List[CommentOut])
def read_comments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    comments = get_comments(db, skip=skip, limit=limit)
    return comments

@router.put("/{comment_id}", response_model=CommentOut)
def update_existing_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)):
    return update_comment(db=db, comment_id=comment_id, comment=comment)

@router.delete("/{comment_id}", response_model=CommentOut)
def delete_existing_comment(comment_id: int, db: Session = Depends(get_db)):
    return delete_comment(db=db, comment_id=comment_id)
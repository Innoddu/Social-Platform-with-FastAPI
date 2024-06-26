from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.comment import CommentResponse, CommentCreate, CommentUpdate
from services import auth_service, comment_service
from config.db import get_db
from typing import List

router = APIRouter()

@router.post("/create", response_model=CommentResponse)
async def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    email: str = Depends(auth_service.get_current_user_authorization),
):
    return await comment_service.create_comment(db, comment, email)


@router.get("/feed/{feed_id}", response_model=List[CommentResponse])
async def get_comments_by_feed_id(feed_id: int, db: Session = Depends(get_db)):
    return await comment_service.get_comment_by_feed_id(db, feed_id)


@router.patch("/update/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    email: str = Depends(auth_service.get_current_user_authorization),
):
    return await comment_service.update_comment(db, comment_id, comment, email)


@router.delete("/delete/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    email: str = Depends(auth_service.get_current_user_authorization),
):
    await comment_service.delete_comment(db, comment_id, email)
    return {"message": "Comment Deleted"}
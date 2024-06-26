from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.feed import FeedCreate, FeedResponse, FeedUpdate, Feed
from services import feed_service, auth_service
from config.db import get_db
from typing import List

router = APIRouter()

@router.post("/create", response_model=FeedResponse)
async def create(feed: FeedCreate, db: AsyncSession=Depends(get_db), email: str=Depends(auth_service.get_current_user_authorization)):
    print(email)
    if email is None:
        raise HTTPException(status_code=401, detail="Not authorized!!!!")
    return await feed_service.create_feed(db, feed, email)

@router.get("/read/{feed_id}", response_model=FeedResponse)
async def read_feed(feed_id: int, db: AsyncSession=Depends(get_db)):
    return await feed_service.get_feed_by_id(db, feed_id)

@router.get("/list", response_model=List[FeedResponse])
async def list_feed(db: AsyncSession=Depends(get_db)):
    return await feed_service.get_feeds(db)

@router.patch("/update/{feed_id}", response_model=FeedResponse)
async def update(feed_id: int, feed: FeedUpdate, db: AsyncSession=Depends(get_db), email: str=Depends(auth_service.get_current_user_authorization)):
    if email is None:
        raise HTTPException(status_code=401, detail="Not authorized") 
    return await feed_service.get_update(db, feed_id, feed, email)

@router.delete("/delete/{feed_id}")
async def delete(feed_id: int, db: AsyncSession=Depends(get_db), email: str=Depends(get_db)):
    if email is None:
        raise HTTPException(status_code=401, detail="Not authorized")
    await feed_service.delete_feed(db, feed_id, email)
    return {"message": "Feed deleted successfully"}

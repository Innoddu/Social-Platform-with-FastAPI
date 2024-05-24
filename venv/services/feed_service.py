from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import join
from models.feed import FeedCreate, FeedUpdate
from models.user import User, Feed

def create_feed(db: Session, feed: FeedCreate, author_email: str):
    feed_dict = feed.model_dump()
    feed_dict["author_email"] = author_email

    author = db.query(User).filter(User.email == author_email).first()

    if author is None:
        raise HTTPException(status_code=404, detail="Author Not Found")
    
    author_id = author.id

    db_feed = Feed(**feed_dict)
    db.add(db_feed)
    db.commit()
    db.refresh(db_feed)

    return {
        "id": db_feed.id,
        "title": db_feed.title,
        "content": db_feed.content,
        "author_email": db_feed.author_email,
        "author_id": db_feed.author_id,
    }

def get_feed_by_id(db: Session, feed_id: int):
    feed_data = (
        db.query(Feed, User.id).join(User, User.email == Feed.author_email).filter(Feed.id == feed_id).first()
    )

    if feed_data is None:
        raise HTTPException(status=404, detail="Feed Not Found")

    feed, id = feed_data

    return {
        "id": feed.id,
        "title": feed.title,
        "content": feed.content,
        "author_email": feed.author_email,
        "author_id": id
    }

def get_feeds(db: Session):
    feeds = db.query(Feed, User.id).join(User, User.email == Feed.author_email).all()
    feed_response = []

    for feed, id in feeds:
        feed_dict = {
            "id": feed.id,
            "title": feed.title,
            "content": feed.content,
            "author_email": feed.author_email,
            "author_id": id
        }
        feed_response.append(feed_dict)
    return feed_response

def get_update(db: Session, feed_id: int, feed_update: FeedUpdate, email: str):
    db_feed = db.query(Feed).filter(Feed.id == feed_id).first()

    if db_feed is None:
        raise HTTPException(status_code=404, detail="Feed Not Found")
    if db_feed.author_email != email:
        raise HTTPException(status_code=403, detail="Permission Denied")

    author = db.query(User).filter(User.email == email).first()
    author_id = author.id

    db_feed.title = feed_update.title
    db_feed.content = feed_update.content
    db_feed.author_id = author_id

    db.commit()
    db.refresh(db_feed)

    return {
        "id": db_feed.id,
        "title": db_feed.title,
        "content": db_feed.content,
        "author_email": db_feed.author_email,
        "author_id": author_id,
    }

def delete_feed(db: Session, feed_id: int, email: str):
    db_feed = db.query(Feed).filter(Feed.id == feed_id).first()

    if db_feed is None:
        raise HTTPException(status_code=404, detail="Feed Not Found")
    if db_feed.author_email != email:
        raise HTTPException(status_code=403, detail="Permission Denied")
    
    db.delete(db_feed)
    db.commit()

    
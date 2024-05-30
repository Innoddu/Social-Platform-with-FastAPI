from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import join
from sqlalchemy.future import select
from models.feed import Feed, FeedCreate, FeedUpdate
from models.user import User

async def create_feed(db: Session, feed: FeedCreate, author_email: str):
    feed_dict = feed.model_dump()
    feed_dict["author_email"] = author_email

    # author = db.query(User).filter(User.email == author_email).first()

    # async
    author = db.execute(select(User).where(User.email == author_email))
    author = author.scalar_one_or_none()

    if author is None:
        raise HTTPException(status_code=404, detail="Author Not Found")

    author_name = author.name

    db_feed = Feed(**feed_dict)
    db.add(db_feed)
    db.commit()
    db.refresh(db_feed)

    return {
        "id": db_feed.id,
        "title": db_feed.title,
        "content": db_feed.content,
        "author_email": db_feed.author_email,
        "author_name": author_name,
    }

async def get_feed_by_id(db: Session, feed_id: int):
    # feed_data = (
    #     db.query(Feed, User.name).join(User, User.email == Feed.author_email).filter(Feed.id == feed_id).first()
    # )
    # async
    feed_data = db.execute(select(Feed, User.name).join(User, User.email == Feed.author_email).where(Feed.id == feed_id))
    feed_data = feed_data.first()

    if feed_data is None:
        raise HTTPException(status=404, detail="Feed Not Found")

    feed, name = feed_data

    return {
        "id": feed.id,
        "title": feed.title,
        "content": feed.content,
        "author_email": feed.author_email,
        "author_id": name
    }

async def get_feeds(db: Session):
    # feeds = db.query(Feed, User.name).join(User, User.email == Feed.author_email).all()

    # async
    feeds = db.execute(select(Feed, User.name).join(User, User.email == Feed.author_email))
    feed_response = []

    for feed, name in feeds:
        feed_dict = {
            "id": feed.id,
            "title": feed.title,
            "content": feed.content,
            "author_email": feed.author_email,
            "author_name": name
        }
        feed_response.append(feed_dict)
    return feed_response

async def get_update(db: Session, feed_id: int, feed_update: FeedUpdate, email: str):
    # db_feed = db.query(Feed).filter(Feed.id == feed_id).first()

    # async
    db_feed = await db.execute(select(Feed).where(Feed.id == feed_id))
    db_feed = db_feed.scalar_one_or_none()

    if db_feed is None:
        raise HTTPException(status_code=404, detail="Feed Not Found")
    if db_feed.author_email != email:
        raise HTTPException(status_code=403, detail="Permission Denied")

    # author = db.query(User).filter(User.email == email).first()
    # author_name = author.name

    # async
    author_res = await db.execute(select(User).where(User.email == email))
    author = author_res.scalar_one_or_none()
    author_name = author.name

    db_feed.title = feed_update.title
    db_feed.content = feed_update.content

    await db.commit()
    await db.refresh(db_feed)

    return {
        "id": db_feed.id,
        "title": db_feed.title,
        "content": db_feed.content,
        "author_email": db_feed.author_email,
        "author_name": author_name,
    }

async def delete_feed(db: Session, feed_id: int, email: str):
    # db_feed = db.query(Feed).filter(Feed.id == feed_id).first()

    # async
    res = await db.execute(select(Feed).where(Feed.id == feed_id))
    db_feed = res.scalars().first()

    if db_feed is None:
        raise HTTPException(status_code=404, detail="Feed Not Found")
    if db_feed.author_email != email:
        raise HTTPException(status_code=403, detail="Permission Denied")
    
    await db.delete(db_feed)
    await db.commit()

    
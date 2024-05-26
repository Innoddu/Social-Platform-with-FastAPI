from email.policy import HTTP
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.comment import Comment, CommentCreate, CommentUpdate, CommentResponse
from models.user import User
from models.feed import Feed
import logging

logging.basicConfig(level=logging.DEBUG)

def create_comment(db: Session, comment: CommentCreate, author_email: str):
    comment_dict = comment.model_dump()
    comment_dict['author_email'] = author_email

    author = db.query(User).filter(User.email == author_email).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author Not Found")

    author_name = author.name if author else "Unknown"

    feed = db.query(Feed).filter(Feed.id == comment.feed_id).first()
    if feed is None:
        raise HTTPException(status_code=404, detailed="Feed Not Found")
    
    db_comment = Comment(**comment_dict)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return {
        "id": db_comment.id,
        "content": db_comment.content,
        "author_email": db_comment.author_email,
        "author_name": author_name,
        "feed_id": db_comment.feed_id
    }


def get_comment_by_email(db: Session, feed_id: int):
    comments = db.query(Comment).filter(Comment.feed_id == feed_id).all()
    comment_res = []

    for comment in comments:
        author = db.query(User).filter(User.email == comment.author_email).first()
        author_name =author.name
        comment_res.append(
            {
                "id": comment.id,
                "content": comment.content,
                "author_email": comment.author_email,
                "author_name": author_name,
                "feed_id": comment.feed_id
            }
        )
    return comment_res

def update_comment(db: Session, comment_id: int, comment_update: CommentUpdate, email: str):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment Not Exsist")
    if db_comment.author_email != email:
        raise HTTPException(status_code=403, detail="Permission deined")

    db_comment.content = comment_update or db_comment.content
    db.commit()
    db.refresh(db_comment)

    author = db.query(User).filter(User.email == email).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author Not Found")
    
    author_name = author.name

    return {
        "id": db_comment.id,
        "content": db_comment.content,
        "author_email": db_comment.author_email,
        "author_name": author_name,
        "feed_id": db_comment.feed_id
    }

def delete_comment(db: Session, comment_id: int, email: str):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment Not Found")

    if db_comment.author_email != email:
        raise HTTPException(status_code=403, detail="Permission Denied")

    db.delete(db_comment)
    db.commit()
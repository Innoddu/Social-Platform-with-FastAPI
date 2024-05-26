from sqlalchemy import Column, String, Integer, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from config.db import Base
from pydantic import BaseModel
from typing import List, Optional


class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author_email = Column(String, ForeignKey("users.email"))

    author = relationship("User", back_populates="feeds")
    comments = relationship("Comment", back_populates="feed", post_update=True)

class FeedCreate(BaseModel):
    title: str
    content: str

class FeedUpdate(BaseModel):
    title: str
    content: str

class FeedInDB(FeedCreate):
    pass

class FeedResponse(FeedCreate):
    id: int
    author_email: str
    author_name: str
    
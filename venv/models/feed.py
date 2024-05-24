from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base
from pydantic import BaseModel



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
    title: str
    content: str
    author_email: str
    author_id: str
    
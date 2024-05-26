from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from config.db import Base
from pydantic import BaseModel, validator
import re


# Base = declarative_base()


class User(Base):
    __tablename__="users"

    email = Column(String, primary_key=True, index=True)
    password = Column(String())
    name = Column(String())

    # 1:N
    feeds = relationship("Feed", back_populates="author")
    comments = relationship("Comment", back_populates="author", post_update=True)




class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserResponse(BaseModel):
    email: str
    name: str

class UserInDB(UserCreate):
    pass

class UserLogin(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invaild Email Format")
        return value



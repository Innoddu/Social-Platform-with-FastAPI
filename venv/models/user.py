from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, validator
from config.db import Base
import re

Base = declarative_base()

class User(Base):
    __tablename__="users"

    email = Column(String, primary_key=True, index=True)
    password = Column(String())
    id = Column(String())

    # 1:N
    feeds = relationship("Feed", back_populates="author")

class UserCreate(BaseModel):
    email: str
    password: str
    id: str

class UserResponse(BaseModel):
    email: str
    id: str

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



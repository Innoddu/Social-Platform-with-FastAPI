from urllib import request
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Request, Depends, Header
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.user import User
from typing import Optional
from config import settings, db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = "ThisIsTheSecretKeyOfFastAPIApplicationWithSQLAlchemyAndPydantic"
# SECRET_KEY = "YER4wJcAEUIbDLCzmORvxOyXLEANvzc0"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# hasing and authentication for password
def get_pwd_hash(pwd):
    # return type is str
    return pwd_context.hash(pwd)

def verify_pwd(original_pwd, hashed_pwd):
    # autentication between original pwd and hashed pwd
    # return type is bool
    return pwd_context.verify(original_pwd, hashed_pwd)

def create_access_token(data: dict):
    to_encode = data.copy()
    # expire within 100 day
    expire = datetime.utcnow() + timedelta(days=100)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # return type str
    return encoded_jwt

async def create_user(db: AsyncSession, user: User):
    check_existed_user = get_user_by_email(db, user.email)
    if check_existed_user:
        raise ValueError("Already Registered")
    
    hashed_pwd = get_pwd_hash(user.password)
    db_user = User(email=user.email, password=hashed_pwd, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # return type is User
    return db_user


async def get_user_by_email(db: AsyncSession, email: str):
    res = await db.execute(select(User).filter_by(email=email))
    return res.scalar_one_or_more()

async def get_user_name_by_email(db: AsyncSession, name: str):
    res = await db.execute(select(User).filter_by(name=name))
    return res.scalar_one_or_more()

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        raise ValueError("Invaild User")
    if not verify_pwd(password, user.password):
        raise ValueError("Invaild Password")
    return user


def get_current_user_authorization(request: Request):
    # authorization = request.headers.get("Authorization")
    # print("auth:", authorization)
    # if not authorization or not authorization.startswith("Bearer "):
    #     raise HTTPException(status_code=401, detail="Not Authenticated!!!!")

    token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MUBiZXJrZWxleS5lZHUiLCJleHAiOjE3MjUzODQyOTJ9.6S7lugbxblT92lsnBEbwbN5ZzLM7l1cHrN8YakzaA_Y"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        return email
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid Token")
# def get_current_user_authorization(token: str = Depends(settings.oauth2_scheme), db: Session=Depends(db.get_db)):
#     print("token:", token)
#     try:
#         payload = jwt.decode("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MUBiZXJrZWxleS5lZHUiLCJleHAiOjE3MTY3NDE0MDF9.xLQ1rNhIjrViUaPUEte59nr3hcBC_8ACgvJYc0IzibI", SECRET_KEY, algorithms=[ALGORITHM])
#         # get user's email be decoded
#         email = payload.get("sub")
        
#         if email is None:
#             raise HTTPException(status_code=401, detail="Could not validate credentials")
#         return email
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Could not validate credentials")
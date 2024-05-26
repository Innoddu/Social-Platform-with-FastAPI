from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config import db as config
from models.user import UserCreate, UserLogin, UserResponse
from services import auth_service

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(config.get_db)):
    try:
        # Check valid Email and Id
        check_existed_email = auth_service.get_user_by_email(db, user.email)
        check_existed_name = auth_service.get_user_name_by_email(db, user.name)

        if check_existed_email:
            raise HTTPException(status_code=400, detail="Email Already Registered")
        if check_existed_name:
            raise HTTPException(status_code=400, detail="Id Already Existed")
        
        db_user = auth_service.create_user(db, user)
        return {"email" : db_user.email, "name": db_user.name}
    except ValueError:
        raise HTTPException(status_code=400, detail="Already Registered")

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(config.get_db)):
    try:
        db_user = auth_service.authenticate_user(db, user.email, user.password)
    except ValueError:
        raise HTTPException(status_code=401, detail="invaild Credentials")

    access_token = auth_service.create_access_token({"sub": user.email})
    return {"access_token": access_token, "email": db_user.email, "name": db_user.name}
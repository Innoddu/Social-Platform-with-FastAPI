from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.user import User

SECRET_KEY = "thisisTheSecretkeyOfFastAPI"
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
    # expire within 1 day
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # return type str
    return encoded_jwt

def create_user(db: Session, user: User):
    check_existed_user = get_user_by_email(db, user.email)
    if check_existed_user:
        raise ValueError("Already Registered")
    
    hashed_pwd = get_pwd_hash(user.password)
    db_user = User(email=user.email, password=hashed_pwd, id=user.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # return type is User
    return db_user

# inquerying users by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Invaild Credentials")
    if not verify_pwd(password, user.password):
        raise ValueError("Invaild Credentials")
    return user
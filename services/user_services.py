from db.database import SessionLocal
from models.orm import UserORM
from models.schemas import User
from fastapi.security import HTTPBearer
from passlib.context import CryptContext



#Context for handle password hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: SessionLocal, email: str) -> User:
    return db.query(UserORM).filter(UserORM.email == email).first()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: SessionLocal, user: User) -> User:
    userNew = UserORM(**user.model_dump())
    db.add(userNew)
    db.commit()
    db.refresh(userNew)
    return userNew

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import hashlib
import secrets

from app.core.config import settings
from .models import User
from .schemas import UserCreate, TokenData

# Упрощенное хеширование паролей (временно)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Временное решение - простое сравнение
    # В продакшене заменить на bcrypt
    return hash_password(plain_password) == hashed_password

def hash_password(password: str) -> str:
    # Временное решение - используем SHA256 с солью
    # В продакшене заменить на bcrypt
    salt = "temp_salt_change_in_production"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: UserCreate) -> User:
    hashed_password = hash_password(user_data.password)
    db_user = User(
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        role=user_data.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
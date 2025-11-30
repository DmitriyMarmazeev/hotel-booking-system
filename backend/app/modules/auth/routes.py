from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from . import services, schemas
from .dependencies import get_current_active_user
from .models import User

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    # Check if user already exists
    db_user = services.get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return services.create_user(db=db, user_data=user_data)

@router.post("/login", response_model=schemas.Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = services.create_access_token(
        data={"sub": str(user.id)}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_active_user
from app.modules.auth.models import User
from . import services, schemas
from .dependencies import get_current_admin_user

router = APIRouter()

# Публичные эндпоинты (требуют аутентификации)
@router.get("/profile", response_model=schemas.UserProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user_profile = services.get_user_profile(db, current_user.id)
    if not user_profile:
        raise HTTPException(status_code=404, detail="User not found")
    return user_profile

@router.put("/profile", response_model=schemas.UserResponse)
def update_my_profile(
    user_update: schemas.UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    updated_user = services.update_user_profile(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# Административные эндпоинты
@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    return services.get_all_users(db, skip=skip, limit=limit)

@router.put("/{user_id}/role", response_model=schemas.UserResponse)
def update_user_role(
    user_id: str,
    role_update: schemas.UserRoleUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    updated_user = services.update_user_role(db, user_id, role_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    success = services.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_active_user
from app.modules.auth.models import User

# Проверка прав администратора
async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Проверка прав менеджера или администратора
async def get_current_manager_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role not in ['hotel_manager', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
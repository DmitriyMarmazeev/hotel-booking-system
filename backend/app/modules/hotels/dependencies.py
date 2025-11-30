from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_active_user
from app.modules.auth.models import User
from . import services, models  # Добавляем импорт models

# Проверка, что пользователь является менеджером отеля
async def get_hotel_manager(
    hotel_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> models.Hotel:
    hotel = services.get_hotel(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    if hotel.manager_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to manage this hotel"
        )
    
    return hotel

# Проверка, что пользователь может управлять отелями
async def get_hotel_owner_or_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role not in ['hotel_manager', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to manage hotels"
        )
    return current_user
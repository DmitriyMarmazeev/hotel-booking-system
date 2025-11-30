from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_active_user
from app.modules.auth.models import User
from app.modules.hotels.dependencies import get_hotel_manager
from app.modules.hotels.models import Hotel  # Импортируем Hotel из модуля отелей
from . import services, models

async def get_booking_for_user(
    booking_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> models.Booking:
    """Проверяет, что пользователь имеет доступ к бронированию"""
    booking = services.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Пользователь может видеть свои бронирования или быть менеджером отеля/админом
    if (booking.guest_id != current_user.id and 
        current_user.role not in ['hotel_manager', 'admin']):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this booking"
        )
    
    return booking

async def get_booking_for_hotel_manager(
    booking_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> models.Booking:
    """Проверяет, что пользователь является менеджером отеля для этого бронирования"""
    booking = services.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Проверяем, что текущий пользователь - менеджер отеля, к которому относится бронирование
    if (booking.room.hotel.manager_id != current_user.id and 
        current_user.role != 'admin'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to manage this booking"
        )
    
    return booking
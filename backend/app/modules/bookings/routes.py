from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_active_user, get_current_user
from app.modules.auth.models import User
from app.modules.users.dependencies import get_current_admin_user
from app.modules.hotels.dependencies import get_hotel_manager
from app.modules.hotels.models import Hotel
from . import services, schemas, models
from .dependencies import get_booking_for_user, get_booking_for_hotel_manager
from app.shared.schemas import UserShortInfo

router = APIRouter()

# Бронирования для гостей
@router.post("/", response_model=schemas.BookingResponse)
def create_booking(
    booking_data: schemas.BookingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        return services.create_booking(db, booking_data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-bookings", response_model=List[schemas.BookingResponse])
async def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: UserShortInfo = Depends(get_current_user)
):
    """Получить мои бронирования"""
    bookings = services.get_user_bookings(db, current_user.id)
    return bookings

@router.get("/{booking_id}", response_model=schemas.BookingResponse)  # Используем BookingResponse
def get_booking(
    booking: models.Booking = Depends(get_booking_for_user),
    db: Session = Depends(get_db)
):
    return booking

@router.put("/{booking_id}/cancel", response_model=schemas.BookingResponse)
def cancel_booking(
    booking: models.Booking = Depends(get_booking_for_user),
    db: Session = Depends(get_db)
):
    # Можно отменять только pending или confirmed бронирования
    if booking.status not in ['pending', 'confirmed']:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot cancel booking with status: {booking.status}"
        )
    
    updated_booking = services.update_booking_status(db, booking.id, 'cancelled')
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking

# Управление бронированиями для менеджеров отелей
@router.get("/hotel/{hotel_id}/bookings", response_model=List[schemas.BookingResponse])  # Используем BookingResponse
def get_hotel_bookings(
    hotel_id: UUID,
    hotel: Hotel = Depends(get_hotel_manager),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    bookings = services.get_hotel_bookings(db, hotel_id)
    if status:
        bookings = [b for b in bookings if b.status == status]
    return bookings

@router.put("/{booking_id}/status", response_model=schemas.BookingResponse)
def update_booking_status(
    booking_id: UUID,
    status_update: schemas.BookingUpdate,
    booking: models.Booking = Depends(get_booking_for_hotel_manager),
    db: Session = Depends(get_db)
):
    if status_update.status not in ['pending', 'confirmed', 'cancelled', 'completed']:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    updated_booking = services.update_booking_status(db, booking.id, status_update.status)
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking

# Платежи
@router.post("/payments/", response_model=schemas.PaymentResponse)
def create_payment(
    payment_data: schemas.PaymentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Проверяем, что пользователь имеет доступ к бронированию
    booking = services.get_booking(db, payment_data.booking_id)
    if not booking or booking.guest_id != current_user.id:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return services.create_payment(db, payment_data)

@router.put("/payments/{payment_id}/status", response_model=schemas.PaymentResponse)
def update_payment_status(
    payment_id: UUID,
    status: str = Query(..., description="New payment status"),
    transaction_id: Optional[str] = Query(None),
    current_user: User = Depends(get_current_admin_user),  # Только админы могут менять статус платежей
    db: Session = Depends(get_db)
):
    if status not in ['pending', 'completed', 'failed', 'refunded']:
        raise HTTPException(status_code=400, detail="Invalid payment status")
    
    updated_payment = services.update_payment_status(db, payment_id, status, transaction_id)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment

# Проверка доступности
@router.get("/availability/check")
def check_availability(
    room_id: UUID,
    check_in: date,
    check_out: date,
    db: Session = Depends(get_db)
):
    is_available = services.check_room_availability(db, room_id, check_in, check_out)
    price = services.calculate_booking_price(db, room_id, check_in, check_out, 1)  # Базовый расчет для 1 гостя
    
    return {
        "available": is_available,
        "estimated_price": price,
        "nights": (check_out - check_in).days
    }
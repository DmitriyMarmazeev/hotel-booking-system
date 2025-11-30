from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func

from . import models, schemas
from app.modules.hotels.models import Room, RoomType, Hotel

def get_user_bookings(db: Session, user_id: UUID) -> List[models.Booking]:
    """Получает все бронирования пользователя с загрузкой связанных данных"""
    return db.query(models.Booking).options(
            # Загружаем связанные данные для избежания N+1 запросов
            joinedload(models.Booking.room)
                .joinedload(Room.room_type),
            joinedload(models.Booking.room)
                .joinedload(Room.hotel),  # Загружаем отель через номер
            joinedload(models.Booking.guest),
            joinedload(models.Booking.payments)
        ).filter(models.Booking.guest_id == user_id).order_by(models.Booking.created_at.desc()).all()

def get_hotel_bookings(db: Session, hotel_id: UUID) -> List[models.Booking]:
    """Получает все бронирования отеля с загрузкой связанных данных"""
    return db.query(models.Booking).join(Room).options(
            joinedload(models.Booking.room).joinedload(Room.room_type),  # Используем Room из hotels
            joinedload(models.Booking.room).joinedload(Room.hotel),      # Используем Room из hotels
            joinedload(models.Booking.guest),
            joinedload(models.Booking.payments)
        ).filter(Room.hotel_id == hotel_id).order_by(models.Booking.created_at.desc()).all()

def check_room_availability(db: Session, room_id: UUID, check_in: date, check_out: date) -> bool:
    """Проверяет доступность номера на указанные даты"""
    conflicting_bookings = db.query(models.Booking).filter(
        models.Booking.room_id == room_id,
        models.Booking.status.in_(['pending', 'confirmed']),
        or_(
            and_(models.Booking.check_in_date < check_out, models.Booking.check_out_date > check_in)
        )
    ).count()
    
    return conflicting_bookings == 0

def calculate_booking_price(db: Session, room_id: UUID, check_in: date, check_out: date, guests: int) -> float:
    """Рассчитывает общую стоимость бронирования"""
    room = db.query(Room).filter(Room.id == room_id).first()  # Используем Room из hotels
    if not room:
        raise ValueError("Room not found")
    
    # Простой расчет: цена за ночь * количество ночей
    nights = (check_out - check_in).days
    if nights <= 0:
        raise ValueError("Invalid date range")
    
    # Проверяем, что номер вмещает указанное количество гостей
    if guests > room.room_type.capacity:
        raise ValueError(f"Room capacity is {room.room_type.capacity} guests")
    
    total_price = room.room_type.base_price * nights
    return total_price

def create_booking(db: Session, booking_data: schemas.BookingCreate, guest_id: UUID) -> models.Booking:
    """Создает новое бронирование"""
    # Проверяем доступность номера
    if not check_room_availability(db, booking_data.room_id, booking_data.check_in_date, booking_data.check_out_date):
        raise ValueError("Room is not available for the selected dates")
    
    # Рассчитываем цену
    total_price = calculate_booking_price(
        db, booking_data.room_id, 
        booking_data.check_in_date, booking_data.check_out_date,
        booking_data.number_of_guests
    )
    
    # Создаем бронирование
    db_booking = models.Booking(
        **booking_data.dict(),
        guest_id=guest_id,
        total_price=total_price,
        status='pending'
    )
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def get_booking(db: Session, booking_id: UUID) -> Optional[models.Booking]:
    """Получает бронирование по ID"""
    return db.query(models.Booking)\
        .options(
            joinedload(models.Booking.room).joinedload(Room.room_type),
            joinedload(models.Booking.room).joinedload(Room.hotel),
            joinedload(models.Booking.guest),
            joinedload(models.Booking.payments)
        )\
        .filter(models.Booking.id == booking_id)\
        .first()

def update_booking_status(db: Session, booking_id: UUID, status: str) -> Optional[models.Booking]:
    """Обновляет статус бронирования"""
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not db_booking:
        return None
    
    db_booking.status = status
    if status == 'cancelled':
        db_booking.cancelled_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_booking)
    return db_booking

def create_payment(db: Session, payment_data: schemas.PaymentCreate) -> models.Payment:
    """Создает запись о платеже"""
    db_payment = models.Payment(**payment_data.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def update_payment_status(db: Session, payment_id: UUID, status: str, transaction_id: Optional[str] = None) -> Optional[models.Payment]:
    """Обновляет статус платежа"""
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not db_payment:
        return None
    
    db_payment.payment_status = status
    if transaction_id:
        db_payment.transaction_id = transaction_id
    if status == 'completed':
        db_payment.payment_date = datetime.utcnow()
    
    db.commit()
    db.refresh(db_payment)
    return db_payment
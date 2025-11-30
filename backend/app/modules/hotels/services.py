from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, case

from . import models, schemas
from app.modules.bookings.models import Booking, Payment

# Hotel services
def create_hotel(db: Session, hotel_data: schemas.HotelCreate, manager_id: UUID) -> models.Hotel:
    db_hotel = models.Hotel(**hotel_data.dict(), manager_id=manager_id)
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def get_hotel(db: Session, hotel_id: UUID) -> Optional[models.Hotel]:
    return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()

def get_user_hotels(db: Session, manager_id: UUID) -> List[models.Hotel]:
    return db.query(models.Hotel).filter(models.Hotel.manager_id == manager_id).all()

def update_hotel(db: Session, hotel_id: UUID, hotel_update: schemas.HotelUpdate) -> Optional[models.Hotel]:
    db_hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    if not db_hotel:
        return None
    
    update_data = hotel_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_hotel, field, value)
    
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def search_hotels(db: Session, filters: schemas.SearchFilters) -> List[Dict[str, Any]]:
    """Расширенный поиск отелей с учетом доступности номеров"""
    query = db.query(models.Hotel).filter(models.Hotel.is_active == True)
    
    # Базовые фильтры по местоположению
    if filters.city:
        query = query.filter(models.Hotel.city.ilike(f"%{filters.city}%"))
    if filters.country:
        query = query.filter(models.Hotel.country.ilike(f"%{filters.country}%"))
    
    # Фильтры по удобствам
    if filters.amenities:
        for amenity in filters.amenities:
            query = query.filter(models.Hotel.amenities.contains([amenity]))
    
    # Получаем отели
    hotels = query.all()
    
    results = []
    for hotel in hotels:
        # Получаем все доступные номера отеля с учетом фильтров
        available_rooms_query = db.query(models.Room).filter(
            models.Room.hotel_id == hotel.id,
            models.Room.is_available == True
        ).join(models.RoomType)
        
        # Фильтры для номеров
        if filters.guests:
            available_rooms_query = available_rooms_query.filter(
                models.RoomType.capacity >= filters.guests
            )
        
        if filters.check_in and filters.check_out:
            # Исключаем номера с конфликтующими бронированиями
            conflicting_rooms_subquery = db.query(Booking.room_id).filter(
                Booking.room_id == models.Room.id,
                Booking.status.in_(['pending', 'confirmed']),
                or_(
                    and_(
                        Booking.check_in_date < filters.check_out,
                        Booking.check_out_date > filters.check_in
                    )
                )
            ).exists()
            
            available_rooms_query = available_rooms_query.filter(~conflicting_rooms_subquery)
        
        available_rooms = available_rooms_query.all()
        
        if not available_rooms:
            continue  # Пропускаем отели без доступных номеров
        
        # Рассчитываем минимальную цену
        room_prices = []
        for room in available_rooms:
            # Базовая цена типа номера
            base_price = room.room_type.base_price
            
            # Здесь можно добавить динамическое ценообразование
            # на основе дат, спроса и т.д.
            if filters.check_in and filters.check_out:
                nights = (filters.check_out - filters.check_in).days
                if nights > 0:
                    # Простой расчет: цена за ночь * количество ночей
                    room_price = base_price * nights
                    room_prices.append(room_price)
                else:
                    room_prices.append(base_price)
            else:
                room_prices.append(base_price)
        
        min_price = min(room_prices) if room_prices else 0
        
        # Фильтр по цене
        if filters.min_price and min_price < filters.min_price:
            continue
        if filters.max_price and min_price > filters.max_price:
            continue
        
        # Группируем доступные номера по типам для статистики
        room_types_available = {}
        for room in available_rooms:
            room_type_name = room.room_type.name
            if room_type_name not in room_types_available:
                room_types_available[room_type_name] = {
                    'count': 0,
                    'min_price': room.room_type.base_price,
                    'capacity': room.room_type.capacity
                }
            room_types_available[room_type_name]['count'] += 1
        
        results.append({
            "id": hotel.id,
            "name": hotel.name,
            "description": hotel.description,
            "address": hotel.address,
            "city": hotel.city,
            "country": hotel.country,
            "star_rating": hotel.star_rating,
            "amenities": hotel.amenities,
            "images": hotel.images,
            "min_price": min_price,
            "available_rooms": len(available_rooms),
            "room_types_available": room_types_available,
            "total_room_types": len(room_types_available)
        })
    
    # Сортировка результатов
    if filters.min_price or filters.max_price:
        results.sort(key=lambda x: x['min_price'])
    else:
        results.sort(key=lambda x: x['star_rating'] or 0, reverse=True)
    
    return results

def get_hotel_availability(db: Session, hotel_id: UUID, check_in: date, check_out: date, guests: int = 1) -> Dict[str, Any]:
    """Получает детальную информацию о доступности номеров в отеле"""
    hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    if not hotel:
        return {"error": "Hotel not found"}
    
    # Получаем все номера отеля
    rooms_query = db.query(models.Room).filter(
        models.Room.hotel_id == hotel_id,
        models.Room.is_available == True
    ).join(models.RoomType)
    
    if guests:
        rooms_query = rooms_query.filter(models.RoomType.capacity >= guests)
    
    all_rooms = rooms_query.all()
    
    # Фильтруем доступные номера (без конфликтующих бронирований)
    available_rooms = []
    for room in all_rooms:
        # Проверяем конфликтующие бронирования
        conflicting_bookings = db.query(Booking).filter(
            Booking.room_id == room.id,
            Booking.status.in_(['pending', 'confirmed']),
            or_(
                and_(
                    Booking.check_in_date < check_out,
                    Booking.check_out_date > check_in
                )
            )
        ).count()
        
        if conflicting_bookings == 0:
            nights = (check_out - check_in).days
            total_price = room.room_type.base_price * nights if nights > 0 else room.room_type.base_price
            
            available_rooms.append({
                "room_id": room.id,
                "room_number": room.room_number,
                "floor": room.floor,
                "room_type": {
                    "id": room.room_type.id,
                    "name": room.room_type.name,
                    "description": room.room_type.description,
                    "base_price": room.room_type.base_price,
                    "capacity": room.room_type.capacity,
                    "amenities": room.room_type.amenities,
                    "size_sqm": room.room_type.size_sqm,
                    "bed_type": room.room_type.bed_type
                },
                "total_price": total_price,
                "nights": nights,
                "price_per_night": room.room_type.base_price
            })
    
    # Группируем по типам номеров
    room_types_available = {}
    for room in available_rooms:
        room_type_name = room["room_type"]["name"]
        if room_type_name not in room_types_available:
            room_types_available[room_type_name] = {
                "room_type": room["room_type"],
                "available_rooms": [],
                "min_price": room["price_per_night"],
                "total_available": 0
            }
        
        room_types_available[room_type_name]["available_rooms"].append(room)
        room_types_available[room_type_name]["total_available"] += 1
        
        # Обновляем минимальную цену
        if room["price_per_night"] < room_types_available[room_type_name]["min_price"]:
            room_types_available[room_type_name]["min_price"] = room["price_per_night"]
    
    return {
        "hotel": {
            "id": hotel.id,
            "name": hotel.name,
            "city": hotel.city,
            "country": hotel.country,
            "address": hotel.address
        },
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests,
        "total_available_rooms": len(available_rooms),
        "room_types_available": room_types_available,
        "available_rooms": available_rooms
    }

def get_popular_destinations(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
    """Получает популярные направления на основе количества бронирований"""
    # Явно указываем связи между таблицами
    popular_destinations = db.query(
        models.Hotel.city,
        models.Hotel.country,
        func.count(Booking.id).label('booking_count')
    ).select_from(models.Hotel)\
     .join(models.Room, models.Hotel.id == models.Room.hotel_id)\
     .join(Booking, models.Room.id == Booking.room_id)\
     .filter(
        Booking.status.in_(['confirmed', 'completed'])
    ).group_by(
        models.Hotel.city, models.Hotel.country
    ).order_by(
        func.count(Booking.id).desc()
    ).limit(limit).all()
    
    return [
        {
            "city": city,
            "country": country,
            "popularity": booking_count
        }
        for city, country, booking_count in popular_destinations
    ]

# Room Type services
def create_room_type(db: Session, room_type_data: schemas.RoomTypeCreate) -> models.RoomType:
    db_room_type = models.RoomType(**room_type_data.dict())
    db.add(db_room_type)
    db.commit()
    db.refresh(db_room_type)
    return db_room_type

def get_room_types(db: Session) -> List[models.RoomType]:
    return db.query(models.RoomType).all()

# Room services
def create_room(db: Session, room_data: schemas.RoomCreate, hotel_id: UUID) -> models.Room:
    db_room = models.Room(**room_data.dict(), hotel_id=hotel_id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_room(db: Session, room_id: UUID) -> Optional[models.Room]:
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def update_room(db: Session, room_id: UUID, room_update: schemas.RoomUpdate) -> Optional[models.Room]:
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
    
    update_data = room_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_room, field, value)
    
    db.commit()
    db.refresh(db_room)
    return db_room
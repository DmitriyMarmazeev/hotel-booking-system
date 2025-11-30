from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import date

from app.core.database import get_db
from app.modules.auth.dependencies import get_current_active_user
from app.modules.auth.models import User
from app.modules.users.dependencies import get_current_admin_user
from . import services, schemas, models
from .dependencies import get_hotel_owner_or_admin, get_hotel_manager

router = APIRouter()

# Public endpoints - поиск отелей
# Добавляем новые эндпоинты поиска
@router.get("/availability/{hotel_id}", response_model=schemas.HotelAvailabilityResponse)
def get_hotel_availability(
    hotel_id: UUID,
    check_in: date,
    check_out: date,
    guests: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """Получает детальную информацию о доступности номеров в конкретном отеле"""
    availability = services.get_hotel_availability(db, hotel_id, check_in, check_out, guests)
    if "error" in availability:
        raise HTTPException(status_code=404, detail=availability["error"])
    return availability

@router.get("/destinations/popular", response_model=List[schemas.PopularDestination])
def get_popular_destinations(
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db)
):
    """Получает популярные направления"""
    return services.get_popular_destinations(db, limit)

# Обновляем существующий эндпоинт поиска
@router.get("/search", response_model=List[schemas.HotelSearchResult])
def search_hotels(
    city: Optional[str] = Query(None, description="Город"),
    country: Optional[str] = Query(None, description="Страна"),
    check_in: Optional[date] = Query(None, description="Дата заезда"),
    check_out: Optional[date] = Query(None, description="Дата выезда"),
    guests: Optional[int] = Query(None, description="Количество гостей"),
    min_price: Optional[float] = Query(None, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, description="Максимальная цена"),
    amenities: Optional[str] = Query(None, description="Удобства через запятую"),
    db: Session = Depends(get_db)
):
    filters = schemas.SearchFilters(
        city=city,
        country=country,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        min_price=min_price,
        max_price=max_price,
        amenities=amenities.split(",") if amenities else None
    )
    return services.search_hotels(db, filters)

@router.get("/{hotel_id}", response_model=schemas.HotelResponse)
def get_hotel_details(
    hotel_id: UUID,
    db: Session = Depends(get_db)
):
    hotel = services.get_hotel(db, hotel_id)
    if not hotel or not hotel.is_active:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel

# Hotel management endpoints
@router.post("/", response_model=schemas.HotelResponse)
def create_hotel(
    hotel_data: schemas.HotelCreate,
    current_user: User = Depends(get_hotel_owner_or_admin),
    db: Session = Depends(get_db)
):
    return services.create_hotel(db, hotel_data, current_user.id)

@router.get("/my/hotels", response_model=List[schemas.HotelResponse])
def get_my_hotels(
    current_user: User = Depends(get_hotel_owner_or_admin),
    db: Session = Depends(get_db)
):
    return services.get_user_hotels(db, current_user.id)

@router.put("/{hotel_id}", response_model=schemas.HotelResponse)
def update_hotel(
    hotel_id: UUID,
    hotel_update: schemas.HotelUpdate,
    hotel: models.Hotel = Depends(get_hotel_manager),
    db: Session = Depends(get_db)
):
    updated_hotel = services.update_hotel(db, hotel_id, hotel_update)
    if not updated_hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return updated_hotel

# Room Type management
@router.post("/room-types/", response_model=schemas.RoomTypeResponse)
def create_room_type(
    room_type_data: schemas.RoomTypeCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    return services.create_room_type(db, room_type_data)

@router.get("/room-types/", response_model=List[schemas.RoomTypeResponse])
def get_room_types(db: Session = Depends(get_db)):
    return services.get_room_types(db)

# Room management
@router.post("/{hotel_id}/rooms", response_model=schemas.RoomResponse)
def create_room(
    hotel_id: UUID,
    room_data: schemas.RoomCreate,
    hotel: models.Hotel = Depends(get_hotel_manager),
    db: Session = Depends(get_db)
):
    return services.create_room(db, room_data, hotel_id)

@router.put("/rooms/{room_id}", response_model=schemas.RoomResponse)
def update_room(
    room_id: UUID,
    room_update: schemas.RoomUpdate,
    current_user: User = Depends(get_hotel_owner_or_admin),
    db: Session = Depends(get_db)
):
    updated_room = services.update_room(db, room_id, room_update)
    if not updated_room:
        raise HTTPException(status_code=404, detail="Room not found")
    return updated_room
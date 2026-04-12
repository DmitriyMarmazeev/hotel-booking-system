from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from uuid import UUID
from app.shared.schemas import RoomShortInfo, HotelShortInfo, RoomTypeShortInfo, UserShortInfo

# Base schemas
class RoomTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    base_price: float = Field(gt=0)
    capacity: int = Field(gt=0)
    amenities: List[str] = []
    size_sqm: Optional[int] = None
    bed_type: Optional[str] = None

class RoomBase(BaseModel):
    room_number: str
    floor: Optional[int] = None
    is_available: bool = True

class HotelBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    city: str
    country: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    star_rating: Optional[int] = Field(None, ge=1, le=5)
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    amenities: List[str] = []
    images: List[str] = []

# Request schemas
class HotelCreate(HotelBase):
    pass

class HotelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    amenities: Optional[List[str]] = None
    images: Optional[List[str]] = None
    is_active: Optional[bool] = None

class RoomTypeCreate(RoomTypeBase):
    pass

class RoomCreate(RoomBase):
    room_type_id: UUID

class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    floor: Optional[int] = None
    is_available: Optional[bool] = None

class PricingCreate(BaseModel):
    date: date
    price: float = Field(gt=0)
    is_available: bool = True

class HotelSearchResult(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    address: str
    city: str
    country: str
    star_rating: Optional[int]
    amenities: List[str]
    images: List[str]
    min_price: float
    available_rooms: int
    room_types_available: Dict[str, Any]  # Статистика по типам номеров
    total_room_types: int
    
    class Config:
        from_attributes = True

class RoomAvailability(BaseModel):
    room_id: UUID
    room_number: str
    floor: Optional[int]
    room_type: 'RoomTypeShortInfo'
    total_price: float
    nights: int
    price_per_night: float

class HotelAvailabilityResponse(BaseModel):
    hotel: 'HotelShortInfo'
    check_in: date
    check_out: date
    guests: int
    total_available_rooms: int
    room_types_available: Dict[str, Any]
    available_rooms: List[RoomAvailability]

class PopularDestination(BaseModel):
    city: str
    country: str
    popularity: int

# Обновляем SearchFilters для поддержки дат
class SearchFilters(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    guests: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    amenities: Optional[List[str]] = None
    sort_by: Optional[str] = None  # price, rating, name

    @validator('check_out')
    def validate_dates(cls, v, values):
        if 'check_in' in values and v and values['check_in']:
            if v <= values['check_in']:
                raise ValueError('Check-out date must be after check-in date')
        return v

# Response schemas
class RoomTypeResponse(RoomTypeBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class RoomResponse(RoomBase):
    id: UUID
    hotel_id: UUID
    room_type: RoomTypeResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

class HotelResponse(HotelBase):
    id: UUID
    manager_id: UUID
    is_active: bool
    created_at: datetime
    rooms: List[RoomResponse] = []
    
    class Config:
        from_attributes = True

class HotelSearchResult(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    address: str
    city: str
    country: str
    star_rating: Optional[int]
    amenities: List[str]
    images: List[str]
    min_price: float
    available_rooms: int
    
    class Config:
        from_attributes = True

class AvailabilityResponse(BaseModel):
    room_type: RoomTypeResponse
    available_rooms: int
    price: float
    date: date
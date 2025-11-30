from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID
from app.shared.schemas import RoomShortInfo, HotelShortInfo, RoomTypeShortInfo, UserShortInfo

# Base schemas
class BookingBase(BaseModel):
    check_in_date: date
    check_out_date: date
    number_of_guests: int = Field(gt=0)
    special_requests: Optional[str] = None

    @validator('check_out_date')
    def validate_dates(cls, v, values):
        if 'check_in_date' in values and v <= values['check_in_date']:
            raise ValueError('Check-out date must be after check-in date')
        return v

class PaymentBase(BaseModel):
    amount: float = Field(gt=0)
    payment_method: str
    transaction_id: Optional[str] = None

# Request schemas
class BookingCreate(BookingBase):
    room_id: UUID

class PaymentCreate(PaymentBase):
    booking_id: UUID

class BookingUpdate(BaseModel):
    status: Optional[str] = None
    special_requests: Optional[str] = None

class BookingSearch(BaseModel):
    hotel_id: Optional[UUID] = None
    guest_id: Optional[UUID] = None
    status: Optional[str] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None

# Response schemas
class PaymentResponse(PaymentBase):
    id: UUID
    payment_status: str
    payment_date: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class BookingResponse(BookingBase):
    id: UUID
    guest_id: UUID
    room_id: UUID
    total_price: float
    status: str
    created_at: datetime
    cancelled_at: Optional[datetime]
    
    # Вложенные объекты
    room: 'RoomShortInfo'
    guest: 'UserShortInfo'
    payments: List[PaymentResponse] = []
    
    class Config:
        from_attributes = True

# Для избежания circular imports
BookingResponse.update_forward_refs()
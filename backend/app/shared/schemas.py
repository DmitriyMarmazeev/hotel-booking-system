from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserShortInfo(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    
    class Config:
        from_attributes = True

class HotelShortInfo(BaseModel):
    id: UUID
    name: str
    city: str
    country: str
    address: Optional[str] = None
    
    class Config:
        from_attributes = True

class RoomTypeShortInfo(BaseModel):
    id: UUID
    name: str
    capacity: int
    base_price: float
    
    class Config:
        from_attributes = True

class RoomShortInfo(BaseModel):
    id: UUID
    room_number: str
    room_type: RoomTypeShortInfo
    hotel: HotelShortInfo
    
    class Config:
        from_attributes = True
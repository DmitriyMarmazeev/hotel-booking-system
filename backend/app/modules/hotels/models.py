from sqlalchemy import Column, String, Text, Integer, Boolean, DECIMAL, ForeignKey, Date, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from app.shared.models import BaseModel

class Hotel(BaseModel):
    __tablename__ = "hotels"
    
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False, index=True)
    country = Column(String(100), nullable=False, index=True)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    star_rating = Column(Integer)  # 1-5 stars
    contact_email = Column(String(255))
    contact_phone = Column(String(20))
    amenities = Column(JSONB, default=[])  # ["wi_fi", "parking", "pool"]
    images = Column(JSONB, default=[])     # URLs фотографий
    is_active = Column(Boolean, default=True)
    
    # Связи
    manager_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    manager = relationship("User", backref="managed_hotels")
    rooms = relationship("Room", back_populates="hotel", cascade="all, delete-orphan")

class RoomType(BaseModel):
    __tablename__ = "room_types"
    
    name = Column(String(100), nullable=False)  # "Стандарт", "Люкс"
    description = Column(Text)
    base_price = Column(DECIMAL(10, 2), nullable=False)
    capacity = Column(Integer, nullable=False)  # Максимум гостей
    amenities = Column(JSONB, default=[])       # ["tv", "ac", "minibar"]
    size_sqm = Column(Integer)                  # Площадь
    bed_type = Column(String(50))               # "double", "twin", "king"
    
    # Связи
    rooms = relationship("Room", back_populates="room_type")

class Room(BaseModel):
    __tablename__ = "rooms"
    
    room_number = Column(String(20), nullable=False)  # "101", "201A"
    floor = Column(Integer)
    is_available = Column(Boolean, default=True)
    images = Column(JSONB, default=[])
    
    # Связи
    hotel_id = Column(UUID(as_uuid=True), ForeignKey("hotels.id"), nullable=False)
    room_type_id = Column(UUID(as_uuid=True), ForeignKey("room_types.id"), nullable=False)
    
    hotel = relationship("Hotel", back_populates="rooms")
    room_type = relationship("RoomType", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")

class Pricing(BaseModel):
    __tablename__ = "pricing"
    
    date = Column(Date, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    is_available = Column(Boolean, default=True)
    
    # Связи
    room_type_id = Column(UUID(as_uuid=True), ForeignKey("room_types.id"), nullable=False)
    room_type = relationship("RoomType")
    
    __table_args__ = (UniqueConstraint('room_type_id', 'date', name='unique_room_type_date'),)
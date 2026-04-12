from sqlalchemy import Column, String, Text, Integer, Boolean, DECIMAL, ForeignKey, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.shared.models import BaseModel

class Booking(BaseModel):
    __tablename__ = "bookings"
    
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    number_of_guests = Column(Integer, nullable=False, default=1)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default='pending')  # pending, confirmed, cancelled, completed
    special_requests = Column(Text)
    
    # Связи
    guest_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False)
    
    guest = relationship("User", backref="bookings")
    room = relationship("Room", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking", cascade="all, delete-orphan")
    
    # Отмененные бронирования
    cancelled_at = Column(DateTime)

class Payment(BaseModel):
    __tablename__ = "payments"
    
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)  # card, cash, etc.
    payment_status = Column(String(20), nullable=False, default='pending')  # pending, completed, failed, refunded
    transaction_id = Column(String(255))
    payment_date = Column(DateTime)
    
    # Связи
    booking_id = Column(UUID(as_uuid=True), ForeignKey("bookings.id"), nullable=False)
    booking = relationship("Booking", back_populates="payments")
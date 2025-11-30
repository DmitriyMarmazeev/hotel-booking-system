from sqlalchemy import Column, String, Boolean, DateTime
from app.shared.models import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    role = Column(String(20), nullable=False, default='guest')  # 'guest', 'hotel_manager', 'admin'
    is_active = Column(Boolean, default=True)
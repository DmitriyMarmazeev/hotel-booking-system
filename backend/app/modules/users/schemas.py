from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID

from app.modules.auth.schemas import UserBase

# Request schemas
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

class UserRoleUpdate(BaseModel):
    role: str

# Response schemas (наследуем от auth)
from app.modules.auth.schemas import UserResponse

class UserProfileResponse(UserResponse):
    total_bookings: Optional[int] = 0
    # Можно добавить дополнительную статистику
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import Optional

class UserBase(BaseModel):
    phone_number: str

class UserCreate(UserBase):
    full_name: Optional[str] = None
    password: str = Field(..., min_length=6)

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    full_name: Optional[str] = None

    class Config:
        from_attributes = True

class MechanicProfileBase(BaseModel):
    user_id: UUID
    name: Optional[str] = None
    status: str
    current_location: Optional[str] = None

class MechanicProfileResponse(MechanicProfileBase):
    id: UUID
    rating: Optional[Decimal] = None
    rating_count: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EmergencyRequestCreate(BaseModel):
    customer_phone_number: str
    location: str
    service_type: str
    vehicle_type: str
    description: Optional[str] = None

class EmergencyRequestResponse(EmergencyRequestCreate):
    id: UUID
    status: str
    mechanic_id: Optional[UUID] = None
    requested_at: datetime
    assigned_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

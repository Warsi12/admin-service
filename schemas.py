from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from decimal import Decimal

class UserBase(BaseModel):
    phone_number: str

class UserCreate(UserBase):
    full_name: str
    password: str = Field(..., min_length=6)

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    full_name: str | None = None

    class Config:
        from_attributes = True

class MechanicProfileBase(BaseModel):
    user_id: UUID
    name: str | None = None
    status: str
    current_location: str | None = None

class MechanicProfileResponse(MechanicProfileBase):
    id: UUID
    rating: Decimal | None = None
    rating_count: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EmergencyRequestCreate(BaseModel):
    customer_phone_number: str
    location: str
    service_type: str
    vehicle_type: str
    description: str | None = None

class EmergencyRequestResponse(EmergencyRequestCreate):
    id: UUID
    status: str
    mechanic_id: UUID | None = None
    requested_at: datetime
    assigned_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

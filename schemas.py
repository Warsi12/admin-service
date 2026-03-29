from pydantic import BaseModel, Field

class UserBase(BaseModel):
    phone_number: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

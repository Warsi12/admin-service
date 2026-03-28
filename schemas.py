from pydantic import BaseModel

class UserBase(BaseModel):
    phone_number: str

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

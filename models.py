from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users_web"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

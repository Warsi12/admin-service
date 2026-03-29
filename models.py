import uuid
from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, Text, CheckConstraint, UUID as SA_UUID
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users_web"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)

class MechanicProfile(Base):
    __tablename__ = "mechanics_profile_web"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    name = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, server_default="OFFLINE")
    current_location = Column(String(50))
    rating = Column(Numeric(2, 1), server_default="0.0")
    rating_count = Column(Integer, server_default="0")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(status.in_(['ONLINE', 'BUSY', 'OFFLINE', 'SUSPENDED'])),
    )

class EmergencyRequest(Base):
    __tablename__ = "emergency_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_phone_number = Column(String(15), nullable=False)
    location = Column(String(50), nullable=False)  # "lat,long"
    service_type = Column(String(50), nullable=False)   # e.g. PUNCTURE, TOWING
    vehicle_type = Column(String(30), nullable=False)   # e.g. CAR, BIKE
    status = Column(String(20), nullable=False, server_default="PENDING")
    mechanic_id = Column(UUID(as_uuid=True), nullable=True)
    description = Column(Text, nullable=True)
    requested_at = Column(TIMESTAMP, server_default=func.now())
    assigned_at = Column(TIMESTAMP, nullable=True)
    completed_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(status.in_(['PENDING', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'])),
    )

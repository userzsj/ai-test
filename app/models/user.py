from sqlalchemy import Column, Integer, String, TIMESTAMP, Enum, Boolean
from sqlalchemy.sql import func
import enum
from app.models.base import Base

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    is_verified = Column(Boolean, nullable=False, default=False)
    verification_token = Column(String(255), nullable=True)
    token_expires_at = Column(TIMESTAMP, nullable=True)
    create_time = Column(TIMESTAMP, nullable=False, server_default=func.now())
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: UserRole = Field(UserRole.USER)

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    role: UserRole | None = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_verified: bool
    create_time: datetime

    class Config:
        from_attributes = True

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6)
    captcha_id: str = Field(..., description="验证码ID")
    captcha_text: str = Field(..., description="验证码")
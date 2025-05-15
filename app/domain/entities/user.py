from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr, Field

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    active: Optional[bool] = True
    role: Optional[UserRole] = UserRole.USER

class UserCreateSchema(UserBase):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str
    first_name: str
    last_name: str

class UserUpdateSchema(UserBase):
    password: Optional[str] = None

class UserInDBBaseSchema(UserBase):
    id: UUID = Field(default_factory=uuid4)
    hashed_password: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Config:
        orm_mode = True

class UserResponseSchema(UserInDBBaseSchema):
    hashed_password: Optional[str] = Field(None, exclude=True)

    id: UUID
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime
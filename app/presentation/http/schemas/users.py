from enum import Enum
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class UserCreateApiSchema(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    first_name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z\s'-]+$")
    last_name: str = Field(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z\s'-]+$")

    @field_validator("username")
    @classmethod
    def username_allowed_characters(cls, value):
        if not value.isalnum() and "-" not in value and "_" not in value:
            raise ValueError(
                "Username must contain only alphanumeric characters, hyphens, or underscores."
            )
        return value

    @field_validator("first_name", "last_name")
    @classmethod
    def name_allowed_characters(cls, value, field):
        if (
            not value.isalpha()
            and " " not in value
            and "'" not in value
            and "-" not in value
        ):
            raise ValueError(
                f'{field.name.replace("_", " ").title()} must contain only alphabetic characters, spaces, apostrophes, or hyphens.'
            )
        return value


class UserUpdateApiSchema(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(
        None, min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$"
    )
    first_name: Optional[str] = Field(
        None, min_length=1, max_length=50, pattern=r"^[a-zA-Z\s'-]+$"
    )
    last_name: Optional[str] = Field(
        None, min_length=1, max_length=50, pattern=r"^[a-zA-Z\s'-]+$"
    )
    active: Optional[bool] = None
    role: Optional[UserRole] = None

    @field_validator("username")
    @classmethod
    def username_allowed_characters_update(cls, value):
        if (
            value is not None
            and not value.isalnum()
            and "-" not in value
            and "_" not in value
        ):
            raise ValueError(
                "Username must contain only alphanumeric characters, hyphens, or underscores."
            )
        return value

    @field_validator("first_name", "last_name")
    @classmethod
    def name_allowed_characters_update(cls, value, field):
        if (
            value is not None
            and not value.isalpha()
            and " " not in value
            and "'" not in value
            and "-" not in value
        ):
            raise ValueError(
                f'{field.name.replace("_", " ").title()} must contain only alphabetic characters, spaces, apostrophes, or hyphens.'
            )
        return value

    @field_validator("*", mode="before")
    @classmethod
    def check_at_least_one_value(cls, value, field):
        if value is not None:
            cls._has_data = True
            return value
        return value

    class Config:
        extra = "forbid"

    _has_data: bool = False

    @field_validator("*", mode="before")
    @classmethod
    def at_least_one_field_updated(cls, values):
        if not cls._has_data and not values:
            raise ValueError("Must provide at least one field to update.")
        return values


class UserResponseApiSchema(BaseModel):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    active: bool
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        


class UserListResponseApiSchema(BaseModel):
    users: List[UserResponseApiSchema]


class UserDeleteResponseApiSchema(BaseModel):
    message: str = "User deleted successfully"

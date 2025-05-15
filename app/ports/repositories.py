from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.user import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
    UserRole,
    UserInDBBaseSchema,
)


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[UserInDBBaseSchema]:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserInDBBaseSchema]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserInDBBaseSchema]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserInDBBaseSchema]:
        pass

    @abstractmethod
    def add(self, user_data: UserCreateSchema) -> UserInDBBaseSchema:
        pass

    @abstractmethod
    def update(
        self, user_id: UUID, user_data: UserUpdateSchema
    ) -> Optional[UserInDBBaseSchema]:
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> bool:
        pass

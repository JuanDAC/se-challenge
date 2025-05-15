from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.users import (
    UserCreate,
    UserUpdate,
    UserInDBBase,
)


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[UserInDBBase]:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserInDBBase]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[UserInDBBase]:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserInDBBase]:
        pass

    @abstractmethod
    def add(self, user_data: UserCreate) -> UserInDBBase:
        pass

    @abstractmethod
    def update(self, user_id: UUID, user_data: UserUpdate) -> Optional[UserInDBBase]:
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> bool:
        pass

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
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        active: Optional[bool] = True,
        include_deleted: Optional[bool] = False,
    ) -> List[UserInDBBase]:
        pass

    @abstractmethod
    def add(self, user_data: UserCreate, hashed_password: str) -> UserInDBBase:
        pass

    @abstractmethod
    def update(
        self, user_id: UUID, user_data: UserUpdate, hashed_password: Optional[str]
    ) -> Optional[UserInDBBase]:
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> bool:
        pass

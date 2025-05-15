from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from app.ports.command import Command
from app.domain.entities.users import (
    UserCreate,
    UserUpdate,
    UserResponse,
)
from abc import ABC, abstractmethod
from typing import List


class CreateUserUseCaseSchema(BaseModel):
    user: UserCreate


class GetUserUseCaseSchema(BaseModel):
    user_id: UUID


class ListUsersUseCaseSchema(BaseModel):
    skip: int = 0
    limit: int = 100
    active: Optional[bool] = None


class UpdateUserUseCaseSchema(BaseModel):
    user_id: UUID
    user: UserUpdate


class DeleteUserUseCaseSchema(BaseModel):
    user_id: UUID


class CreateUserUseCase(Command[UserResponse, CreateUserUseCaseSchema], ABC):
    @abstractmethod
    def execute(self) -> UserResponse:
        pass


class GetUserUseCase(Command[Optional[UserResponse], GetUserUseCaseSchema], ABC):
    @abstractmethod
    def execute(self) -> Optional[UserResponse]:
        pass


class ListUsersUseCase(Command[List[UserResponse], ListUsersUseCaseSchema], ABC):
    @abstractmethod
    def execute(self) -> List[UserResponse]:
        pass


class UpdateUserUseCase(Command[Optional[UserResponse], UpdateUserUseCaseSchema], ABC):
    @abstractmethod
    def execute(self) -> Optional[UserResponse]:
        pass


class DeleteUserUseCase(Command[bool, DeleteUserUseCaseSchema], ABC):
    @abstractmethod
    def execute(self) -> bool:
        pass

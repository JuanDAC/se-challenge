import uuid
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List, Optional, Dict
from app.domain.entities.user import (
    UserCreateSchema,
    UserUpdateSchema,
    UserInDBBaseSchema,
)
from app.ports.repositories import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users: Dict[UUID, UserInDBBaseSchema] = {}

    def get_by_id(self, user_id: UUID) -> Optional[UserInDBBaseSchema]:
        return self._users.get(user_id)

    def get_by_username(self, username: str) -> Optional[UserInDBBaseSchema]:
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def get_by_email(self, email: str) -> Optional[UserInDBBaseSchema]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserInDBBaseSchema]:
        all_users = list(self._users.values())
        return all_users[skip : skip + limit]

    def add(self, user_entity: UserCreateSchema) -> UserInDBBaseSchema:
        if self.get_by_username(user_entity.username):
            raise ValueError(
                f"User with username {user_entity.username} already exists"
            )
        if self.get_by_email(user_entity.email):
            raise ValueError(f"User with email {user_entity.email} already exists")

        user_entity.id = user_entity.id or uuid4()
        user_entity.created_at = datetime.now(timezone.utc)
        user_entity.updated_at = datetime.now(timezone.utc)
        self._users[user_entity.id] = user_entity
        return user_entity

    def update(
        self, user_id: UUID, user_update_data: UserUpdateSchema
    ) -> Optional[UserInDBBaseSchema]:
        if user_id not in self._users:
            return None

        existing_user = self._users[user_id]

        if (
            user_update_data.username != existing_user.username
            and self.get_by_username(user_update_data.username)
        ):
            raise ValueError(f"Username {user_update_data.username} already taken")
        if user_update_data.email != existing_user.email and self.get_by_email(
            user_update_data.email
        ):
            raise ValueError(f"Email {user_update_data.email} already taken")

        updated_user = existing_user.model_copy(
            update=user_update_data.model_dump(exclude_unset=True)
        )
        updated_user.updated_at = datetime.now(timezone.utc)

        self._users[user_id] = updated_user
        return updated_user

    def delete(self, user_id: UUID) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def clear(self):
        self._users = {}

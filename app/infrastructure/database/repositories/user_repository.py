from app.ports.repositories import UserRepository
from app.ports.logging import LoggerServicePort
from app.ports.transactional.transaction_executor import TransactionExecutor
from app.ports.transactional.transactionable import Transactionable
from app.domain.entities.users import (
    UserCreate,
    UserUpdate,
    UserInDBBase,
)
from uuid import UUID
from app.infrastructure.database.models import UserModel
from datetime import datetime, timezone
from typing import Optional, List, TypeVar
from injector import inject
from app.domain.exceptions import (
    EmailAlreadyExistsError,
    UserNotFoundError,
    InvalidCredentialsError,
)

Session = TypeVar("Session")


class SQLAlchemyUserRepository(UserRepository, Transactionable):
    """
    SQLAlchemy implementation of the UserRepository.
    Handles database operations for user entities.
    """

    @inject
    def __init__(
        self,
        logger_service: LoggerServicePort,
    ):
        self.logger_service = logger_service
        self.db_handler = TransactionExecutor(logger_service)

    def _get_active_user_by_id(self, db: Session, user_id: UUID) -> Optional[UserModel]:
        """Helper to get an active (not soft-deleted) user by ID."""
        return (
            db.query(UserModel)
            .filter(UserModel.id == user_id, UserModel.deleted_at == None)
            .first()
        )

    def get_by_id(self, user_id: UUID) -> Optional[UserInDBBase]:
        self.logger_service.info(f"Attempting to get user by ID: {user_id}")
        try:
            with self.db_handler.get_session() as db:
                db_user = self._get_active_user_by_id(db, user_id)
                if db_user:
                    self.logger_service.info(f"User found with ID: {user_id}")
                    return db_user.to_pydantic()
                self.logger_service.warning(
                    f"User not found or soft-deleted with ID: {user_id}"
                )
                return None
        except Exception as e:
            self.logger_service.error(
                f"Error getting user by ID {user_id}: {e}", exc_info=True
            )
            return None

    def get_by_username(self, username: str) -> Optional[UserInDBBase]:
        self.logger_service.info(f"Attempting to get user by username: {username}")
        try:
            with self.db_handler.get_session() as db:
                db_user = (
                    db.query(UserModel)
                    .filter(
                        UserModel.username == username, UserModel.deleted_at == None
                    )
                    .first()
                )
                if db_user:
                    self.logger_service.info(f"User found with username: {username}")
                    return db_user.to_pydantic()
                self.logger_service.warning(
                    f"User not found or soft-deleted with username: {username}"
                )
                return None
        except Exception as e:
            self.logger_service.error(
                f"Error getting user by username {username}: {e}", exc_info=True
            )
            return None

    def get_by_email(self, email: str) -> Optional[UserInDBBase]:
        self.logger_service.info(f"Attempting to get user by email: {email}")
        try:
            with self.db_handler.get_session() as db:
                db_user = (
                    db.query(UserModel)
                    .filter(UserModel.email == email, UserModel.deleted_at == None)
                    .first()
                )
                if db_user:
                    self.logger_service.info(f"User found with email: {email}")
                    return db_user.to_pydantic()
                self.logger_service.warning(
                    f"User not found or soft-deleted with email: {email}"
                )
                return None
        except Exception as e:
            self.logger_service.error(
                f"Error getting user by email {email}: {e}", exc_info=True
            )
            return None

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        active: bool = True,
        include_deleted: bool = False,
    ) -> List[UserInDBBase]:
        self.logger_service.info(
            f"Attempting to get all users (skip={skip}, limit={limit}, active={active}, include_deleted={include_deleted})"
        )
        try:
            with self.db_handler.get_session() as db:
                query = db.query(UserModel)
                query = query.filter(UserModel.active == active)
                if not include_deleted:
                    query = query.filter(UserModel.deleted_at == None)

                db_users = (
                    query.order_by(UserModel.created_at.desc())
                    .offset(skip)
                    .limit(limit)
                    .all()
                )
                self.logger_service.info(f"Retrieved {len(db_users)} users.")
                return [user.to_pydantic() for user in db_users]
        except Exception as e:
            self.logger_service.error(f"Error getting all users: {e}", exc_info=True)
            return []

    def add(self, user_data: UserCreate, hashed_password_str: str) -> UserInDBBase:
        self.logger_service.info(f"Attempting to add new user: {user_data.username}")
        db_user = UserModel(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=user_data.role,
            hashed_password=hashed_password_str,
            active=user_data.active if user_data.active is not None else True,
        )
        try:
            with self.db_handler.get_session() as db:
                db.add(db_user)
                db.flush()
                self.logger_service.info(
                    f"User added successfully: {db_user.username} (ID: {db_user.id})"
                )
                return db_user.to_pydantic()
        except Exception as e:
            self.logger_service.error(
                f"Error adding user {user_data.username}: {e}", exc_info=True
            )
            if "ix_users_email" in str(e.orig):
                self.logger_service.warning(f"Email already exists: {user_data.email}")
                raise EmailAlreadyExistsError("Email already exists")
            elif "ix_users_username" in str(e.orig):
                self.logger_service.warning(
                    f"Username already exists: {user_data.username}"
                )
                raise InvalidCredentialsError("Username already exists")
            raise e

    def update(
        self,
        user_id: UUID,
        user_data: UserUpdate,
        new_hashed_password_str: Optional[str] = None,
    ) -> Optional[UserInDBBase]:
        self.logger_service.info(f"Attempting to update user ID: {user_id}")
        try:
            with self.db_handler.get_session() as db:
                db_user = self._get_active_user_by_id(db, user_id)
                if not db_user:
                    self.logger_service.warning(
                        f"User not found or soft-deleted for update with ID: {user_id}"
                    )
                    return None

                update_data = user_data.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    if key == "password":
                        continue
                    setattr(db_user, key, value)

                if new_hashed_password_str:
                    db_user.hashed_password = new_hashed_password_str

                db.add(db_user)
                db.flush()
                self.logger_service.info(
                    f"User updated successfully: {db_user.username} (ID: {user_id})"
                )
                return db_user.to_pydantic()
        except Exception as e:
            self.logger_service.error(
                f"Error updating user {user_id}: {e}", exc_info=True
            )
            raise

    def delete(self, user_id: UUID) -> bool:
        self.logger_service.info(f"Attempting to soft delete user ID: {user_id}")
        try:
            with self.db_handler.get_session() as db:
                db_user = self._get_active_user_by_id(db, user_id)
                if db_user:
                    db_user.deleted_at = datetime.now(timezone.utc)
                    db_user.active = False
                    db.add(db_user)
                    db.flush()
                    self.logger_service.info(
                        f"User soft-deleted successfully: {db_user.username} (ID: {user_id})"
                    )
                    return True
                self.logger_service.warning(
                    f"User not found for soft delete with ID: {user_id}"
                )
                return False
        except Exception as e:
            self.logger_service.error(
                f"Error soft deleting user {user_id}: {e}", exc_info=True
            )
            return False

    def hard_delete(self, user_id: UUID) -> bool:
        self.logger_service.info(f"Attempting to HARD delete user ID: {user_id}")
        try:
            with self.db_handler.get_session() as db:
                db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
                if db_user:
                    db.delete(db_user)
                    db.flush()
                    self.logger_service.info(
                        f"User hard-deleted successfully: {db_user.username} (ID: {user_id})"
                    )
                    return True
                self.logger_service.warning(
                    f"User not found for hard delete with ID: {user_id}"
                )
                return False
        except Exception as e:
            self.logger_service.error(
                f"Error hard deleting user {user_id}: {e}", exc_info=True
            )
            return False

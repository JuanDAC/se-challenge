from injector import inject
from uuid import UUID
from typing import List, Optional

from app.domain.entities.users import UserResponse
from app.ports.use_cases.users import (
    GetUserUseCase,
    ListUsersUseCase,
)

from app.ports.repositories import UserRepository
from app.ports.transactional.transactional_atom import Atom, AtomClass
from app.ports.transactional.transaction_manager import TransactionManagerPort


@Atom.on_class
class GetUser(GetUserUseCase, AtomClass):
    @inject
    def __init__(
        self,
        user_service: UserRepository,
        transaction_manager: TransactionManagerPort,
    ):
        super().__init__()
        self.user_service = user_service
        self.transaction_manager = transaction_manager

    def execute(self) -> Optional[UserResponse]:
        """
        Executes the logic to get a user by their ID.
        """
        user_id: UUID = self.params.user_id
        user = self.user_service.get_by_id(user_id=user_id)
        return user


@Atom.on_class
class ListUsers(ListUsersUseCase, AtomClass):
    @inject
    def __init__(
        self,
        user_service: UserRepository,
        transaction_manager: TransactionManagerPort,
    ):
        super().__init__()
        self.user_service = user_service
        self.transaction_manager = transaction_manager

    def execute(self) -> List[UserResponse]:
        """
        Executes the logic to list users with pagination and filters.
        """
        users = self.user_service.get_all(
            skip=self.params.skip, limit=self.params.limit, active=self.params.active
        )
        return users

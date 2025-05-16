from injector import inject
from uuid import UUID
from typing import Optional

from app.domain.entities.users import UserUpdate, UserResponse
from app.ports.use_cases.users import (
    UpdateUserUseCase,
)

from app.ports.repositories import UserRepository

from app.ports.transactional.transactional_atom import Atom, AtomClass
from app.ports.transactional.transaction_manager import TransactionManagerPort
from app.ports.services.hasher_service_port import HasherServicePort, HashDataSchema


@Atom.on_class
class UpdateUser(UpdateUserUseCase, AtomClass):
    @inject
    def __init__(
        self,
        user_service: UserRepository,
        transaction_manager: TransactionManagerPort,
        hasher_service: HasherServicePort,
    ):
        super().__init__()
        self.user_service = user_service
        self.hasher_service = hasher_service
        self.transaction_manager = transaction_manager

    def execute(self) -> Optional[UserResponse]:
        """
        Executes the logic to update an existing user.
        """
        user_id: UUID = self.params.user_id
        user_update_data: UserUpdate = self.params.user

        if hasattr(user_update_data, "email") and user_update_data.email:
            self.hasher_service.set_params(
                HashDataSchema(data_to_hash=user_update_data.email)
            )
            user_update_data.hashed_password = self.hasher_service.execute()

        updated_user = self.user_service.update(
            user_id=user_id, user_data=user_update_data
        )
        return updated_user

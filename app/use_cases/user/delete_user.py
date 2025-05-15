from injector import inject
from uuid import UUID

from app.ports.use_cases.users import (
    DeleteUserUseCase,
)

from app.ports.repositories import UserRepository

from app.ports.transactional.transactional_atom import Atom, AtomClass
from app.ports.transactional.transaction_manager import TransactionManagerPort


@Atom.on_class
class DeleteUser(DeleteUserUseCase, AtomClass):
    @inject
    def __init__(
        self,
        user_service: UserRepository,
        transaction_manager: TransactionManagerPort,
    ):
        super().__init__()
        self.user_service = user_service
        self.transaction_manager = transaction_manager

    def execute(self) -> bool:
        """
        Executes the logic to delete a user.
        """
        user_id: UUID = self.params.user_id
        success = self.user_service.delete(user_id=user_id)
        return success

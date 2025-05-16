from injector import inject

from app.domain.entities.users import UserCreate, UserResponse
from app.ports.use_cases.users import (
    CreateUserUseCase,
)

from app.ports.repositories import UserRepository

from app.ports.transactional.transactional_atom import Atom, AtomClass
from app.ports.transactional.transaction_manager import TransactionManagerPort
from app.ports.services.hasher_service_port import HasherServicePort, HashDataSchema


@Atom.on_class
class CreateUser(CreateUserUseCase, AtomClass):
    @inject
    def __init__(
        self,
        user_service: UserRepository,
        transaction_manager: TransactionManagerPort,
        hasher_service: HasherServicePort,
    ):
        super().__init__()
        self.user_service = user_service
        self.transaction_manager = transaction_manager
        self.hasher_service = hasher_service

    def execute(self) -> UserResponse:
        """
        Executes the logic to create a new user.
        """
        user_create_data: UserCreate = self.params.user

        if hasattr(user_create_data, "email") and user_create_data.email:
            self.hasher_service.set_params(
                HashDataSchema(data_to_hash=user_create_data.email)
            )
            hashed_password = self.hasher_service.execute()

        created_user = self.user_service.add(user_create_data, hashed_password)

        return created_user

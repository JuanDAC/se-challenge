from injector import Module, inject, singleton
from app.ports.repositories import (
    UserRepository,
)
from app.ports.logging import LoggerServicePort
    
from app.ports.services.hasher_service_port import (
    HasherServicePort,
    VerifyDataServicePort
)

from app.infrastructure.database.repositories.user_repository import (
    SQLAlchemyUserRepository
)
from app.infrastructure.logging import (
    ConsoleLoggerService,
)

from app.infrastructure.security.passlib_data_hasher import (
    PasslibDataHasher,
)

from app.infrastructure.security.passlib_data_verifier import (
    PasslibDataVerifier,
)

class InfrastructureModule(Module):
    def configure(self, binder):

        binder.bind(UserRepository, to=SQLAlchemyUserRepository)
        binder.bind(LoggerServicePort, to=ConsoleLoggerService)
        binder.bind(HasherServicePort, to=PasslibDataHasher)
        binder.bind(VerifyDataServicePort, to=PasslibDataVerifier)



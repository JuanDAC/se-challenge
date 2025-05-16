from injector import Module, inject, singleton
from app.ports.repositories import (
    UserRepository,
)
from app.ports.logging import LoggerServicePort

from app.ports.services.hasher_service_port import (
    HasherServicePort,
    VerifyDataServicePort,
)

from app.infrastructure.database.repositories.user_repository import (
    SQLAlchemyUserRepository,
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
    def __init__(self, *arg, exclude_classes=None, **kwargs):
        super().__init__(*arg, **kwargs)
        self.exclude_classes = exclude_classes or []

    def configure(self, binder):
        super().configure(binder)

        bindings = [
            (UserRepository, SQLAlchemyUserRepository),
            (LoggerServicePort, ConsoleLoggerService),
            (HasherServicePort, PasslibDataHasher),
            (VerifyDataServicePort, PasslibDataVerifier),
        ]

        for interface, implementation in bindings:
            if interface not in self.exclude_classes:
                binder.bind(interface, to=implementation)

import pytest
from fastapi.testclient import TestClient
from app.presentation.http.app import app as fastapi_app
from tests.fixtures.in_memory_user_repository import InMemoryUserRepository
from uuid import uuid4
from injector import Injector, Module, noscope
from app.ports.repositories import UserRepository

from app.config.config_module import ConfigModule
from app.use_cases.use_cases_module import UseCasesModule
from app.infrastructure.infrastructure_module import InfrastructureModule
from app.ports.transactional.transaction_manager import TransactionManagerPort
from contextlib import contextmanager
from typing import Iterable


def in_memory_user_repo():
    repo = InMemoryUserRepository()
    yield repo
    repo.clear()


class TransactionManager(TransactionManagerPort[bool]):
    @contextmanager
    def get_transaction_context(self) -> Iterable[bool]:
        try:
            yield True
        except Exception as e:
            raise e
        finally:
            pass


@pytest.fixture(scope="function")
def client():
    class TestSpecificInfrastructureModule(Module):
        def configure(self, binder):

            binder.bind(UserRepository, to=InMemoryUserRepository, scope=noscope)
            binder.bind(
                TransactionManagerPort,
                to=TransactionManager,
                scope=noscope,
            )

    class AppModule(Module):
        def configure(self, binder):
            super().configure(binder)

            binder.install(ConfigModule(exclude_classes=[TransactionManagerPort]))
            binder.install(InfrastructureModule(exclude_classes=[UserRepository]))
            binder.install(UseCasesModule())
            binder.install(TestSpecificInfrastructureModule())

    test_injector = Injector([AppModule])

    try:
        import app.app_module as app_dependencies_module

        app_dependencies_module.injector = test_injector

    except (ImportError, AttributeError) as e:
        raise ImportError(
            "Could not import the application's dependencies module. "
            "Make sure the path and module name are correct."
        ) from e

    with TestClient(fastapi_app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def unique_user_payload(faker):
    return {
        "username": faker.user_name() + str(uuid4())[:8],
        "email": str(uuid4())[:8] + faker.email(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "role": faker.random_element(elements=("user", "admin", "guest")),
    }


@pytest.fixture(scope="function")
def created_user(client, unique_user_payload):
    response = client.post("/users/", json=unique_user_payload)
    assert response.status_code == 201
    user_data = response.json()

    yield user_data

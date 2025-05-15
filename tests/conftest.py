import pytest
from fastapi.testclient import TestClient
from app.presentation.http.app import app as fastapi_app
from tests.fixtures.in_memory_user_repository import InMemoryUserRepository
from uuid import uuid4
from injector import Injector, Module, provider, singleton
from app.ports.repositories import UserRepository

from app.config.config_module import ConfigModule
from app.use_cases.use_cases_module import UseCasesModule


@pytest.fixture(scope="function")
def in_memory_user_repo():
    repo = InMemoryUserRepository()
    yield repo
    repo.clear()

@pytest.fixture(scope="function")
def client(in_memory_user_repo_instance: InMemoryUserRepository):
    class TestSpecificInfrastructureModule(Module):
        def __init__(self, repo_instance: InMemoryUserRepository):
            self._repo_instance = repo_instance

        @singleton
        @provider
        def provide_user_repository(self) -> UserRepository:
            return self._repo_instance

    test_injector = Injector([
        ConfigModule(),       
        UseCasesModule(),     
        TestSpecificInfrastructureModule(in_memory_user_repo_instance)
    ])

    try:
        import app.app_module as app_dependencies_module 

        app_dependencies_module.instance = test_injector

    except (ImportError, AttributeError) as e:
        raise ImportError(
            "Could not import the application's dependencies module. "
            "Make sure the path and module name are correct."
        ) from e

    with TestClient(fastapi_app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def client_functional(in_memory_user_repo):
    from app.app_module import get_user_repository_dependency # Make sure this exists
    
    original_overrides = fastapi_app.dependency_overrides.copy()
    fastapi_app.dependency_overrides[get_user_repository_dependency] = lambda: in_memory_user_repo
    
    with TestClient(fastapi_app) as c:
        yield c
    
    fastapi_app.dependency_overrides = original_overrides


@pytest.fixture(scope="function")
def unique_user_payload(faker):
    return {
        "username": faker.user_name() + str(uuid4())[:8],
        "email": faker.email() + str(uuid4())[:8],
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "role": faker.random_element(elements=("user", "admin", "guest"))
    }

@pytest.fixture(scope="function")
def created_user(client, unique_user_payload):
    response = client.post("/users/", json=unique_user_payload)
    assert response.status_code == 201
    user_data = response.json()
    
    yield user_data 

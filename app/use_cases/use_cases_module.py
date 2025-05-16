from injector import Module, inject, singleton
from app.ports.use_cases.users import (
    CreateUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
    ListUsersUseCase,
)

from app.use_cases.user.create_user import CreateUser
from app.use_cases.user.get_user import GetUser, ListUsers
from app.use_cases.user.update_user import UpdateUser
from app.use_cases.user.delete_user import DeleteUser


class UseCasesModule(Module):
    def configure(self, binder):
        super().configure(binder)

        binder.bind(CreateUserUseCase, to=CreateUser)
        binder.bind(GetUserUseCase, to=GetUser)
        binder.bind(UpdateUserUseCase, to=UpdateUser)
        binder.bind(DeleteUserUseCase, to=DeleteUser)
        binder.bind(ListUsersUseCase, to=ListUsers)

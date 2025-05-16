from fastapi import APIRouter, Depends, HTTPException, status

from uuid import UUID

from typing import List, Optional

from app.app_module import injector
from app.presentation.http.routers.swagger import (
    CREATE_USER_SWAGGER,
    GET_USER_SWAGGER,
    LIST_USERS_SWAGGER,
    UPDATE_USER_SWAGGER,
    DELETE_USER_SWAGGER,
)
from app.domain.entities.users import UserCreate, UserUpdate, UserResponse
from app.ports.use_cases.users import (
    GetUserUseCase,
    GetUserUseCaseSchema,
    CreateUserUseCase,
    CreateUserUseCaseSchema,
    ListUsersUseCase,
    ListUsersUseCaseSchema,
    UpdateUserUseCase,
    UpdateUserUseCaseSchema,
    DeleteUserUseCase,
    DeleteUserUseCaseSchema,
)
from app.presentation.http.schemas.users import (
    UserCreateApiSchema,
    UserUpdateApiSchema,
    UserResponseApiSchema,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseApiSchema,
    description=CREATE_USER_SWAGGER,
)
def create_user(
    user_data: UserCreateApiSchema,
    create_user_use_case: CreateUserUseCase = Depends(lambda: injector.get(CreateUserUseCase)),
):
    """
    Creates a new user.
    """
    attributes = CreateUserUseCaseSchema(user=UserCreate(**user_data.dict()))
    create_user_use_case.set_params(attributes)
    return create_user_use_case.execute()


@router.get(
    "/{user_id}",
    response_model=UserResponseApiSchema,
    summary="Read user",
    description=GET_USER_SWAGGER,
)
def get_user(
    user_id: UUID,
    get_user_use_case: GetUserUseCase = Depends(lambda: injector.get(GetUserUseCase)),
):
    """
    Retrieves a user by their ID.
    """
    attributes = GetUserUseCaseSchema(user_id=user_id)
    get_user_use_case.set_params(attributes)
    user = get_user_use_case.execute()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserResponseApiSchema(**user.dict())


@router.get(
    "/",
    response_model=List[UserResponseApiSchema],
    summary="Read users",
    description=LIST_USERS_SWAGGER,
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    active: Optional[bool] = True,
    list_users_use_case: ListUsersUseCase = Depends(lambda: injector.get(ListUsersUseCase)),
):
    """
    Retrieves a list of users with support for pagination and filtering.
    """
    attributes = ListUsersUseCaseSchema(skip=skip, limit=limit, active=active)
    list_users_use_case.set_params(attributes)
    return [
        UserResponseApiSchema(**user.dict()) for user in list_users_use_case.execute()
    ]


@router.put(
    "/{user_id}",
    response_model=UserResponseApiSchema,
    summary="Update user",
    description=UPDATE_USER_SWAGGER,
)
def update_user(
    user_id: UUID,
    user_data: UserUpdateApiSchema,
    update_user_use_case: UpdateUserUseCase = Depends(lambda: injector.get(UpdateUserUseCase)),
):
    """
    Updates the information of an existing user.
    """
    attributes = UpdateUserUseCaseSchema(
        user_id=user_id, user=UserUpdate(**user_data.dict(exclude_unset=True))
    )
    update_user_use_case.set_params(attributes)
    updated_user = update_user_use_case.execute()
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserResponseApiSchema(**updated_user.dict())


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description=DELETE_USER_SWAGGER,
)
def delete_user(
    user_id: UUID,
    delete_user_use_case: DeleteUserUseCase = Depends(lambda: injector.get(DeleteUserUseCase)),
):
    """
    Deletes a user from the system.
    """
    attributes = DeleteUserUseCaseSchema(user_id=user_id)
    delete_user_use_case.set_params(attributes)
    if not delete_user_use_case.execute():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return None

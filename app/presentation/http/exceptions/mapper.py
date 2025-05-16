from app.domain.exceptions import (
    EmailAlreadyExistsError,
    UserNotFoundError,
    InvalidCredentialsError,
)

error_mapper = {
    EmailAlreadyExistsError: {
        "status_code": 409,
        "response_key": "detail",
    },
    UserNotFoundError: {
        "status_code": 404,
        "response_key": "detail",
    },
    InvalidCredentialsError: {
        "status_code": 401,
        "response_key": "detail",
    },
    ValueError: {
        "status_code": 422,
        "response_key": "detail",
    },
    TypeError: {
        "status_code": 422,
        "response_key": "detail",
    },
    KeyError: {
        "status_code": 422,
        "response_key": "detail",
    },
    Exception: {
        "status_code": 500,
        "response_key": "detail",
    },
}
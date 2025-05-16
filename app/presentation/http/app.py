from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.http.routers.users import router as users_router
from app.config.environment import get_environment_variables
from app.config.settings import get_settings
from app.presentation.http.exceptions.register import register_exception_handlers_from_config
from app.presentation.http.exceptions.mapper import error_mapper

envs = get_environment_variables()
settings = get_settings()

app = FastAPI(
    root_path=settings.API_V1_STR,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    title=envs.APP_NAME,
    version=envs.API_VERSION,
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)

app.include_router(users_router, tags=["users"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers_from_config(app, error_mapper)
from functools import lru_cache
from pydantic_settings import BaseSettings


class EnvironmentSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_DIALECT: str
    DB_SCHEMA: str
    API_HOST: str
    API_PORT: int
    DEBUG: bool
    SECRET_KEY: str
    APP_NAME: str
    API_VERSION: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        

@lru_cache
def get_environment_variables():
    env = EnvironmentSettings()
    return env

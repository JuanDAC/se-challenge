from functools import lru_cache


class Settings:
    def __init__(self):
        self.API_V1_STR = "/api/v1"


@lru_cache
def get_settings() -> Settings:
    return Settings()

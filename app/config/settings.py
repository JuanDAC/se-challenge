from functools import lru_cache


class Settings:
    def __init__(self):
        self.API_V1_STR = "/api/v1"
        self.crypt_context_settings = {
            "schemes": ["bcrypt"],
            "default": "bcrypt",
            "deprecated": "auto",
            "bcrypt__rounds": 13,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()

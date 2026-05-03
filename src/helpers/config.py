from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_TYPES: List[str]  # ✅ typed properly
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    model_config = SettingsConfigDict(env_file=".env")  # ✅ pydantic v2 way

@lru_cache()  # ✅ cache so .env is only read once
def get_settings() -> Settings:
    return Settings()
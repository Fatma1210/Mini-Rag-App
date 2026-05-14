from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_TYPES: List[str]  # ✅ typed properly
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGODB_URI: str
    MONGODB_DATABASE: str   

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str = None
    OPENAI_API_URL: str = None
    COHERE_API_KEY: str = None
    GROQ_API_KEY: str = None
    GEMINI_API_KEY: str = None
   

    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None

    INPUT_DEFAULT_MAX_CHARACTERS: int = None
    GENERATION_DEFAULT_MAX_TOKENS: int = None
    GENERATION_DEFAULT_TEMPERATURE: float = None

    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str
    VECTOR_DISTANCE_METHOD: str = None

    DEFAULT_LANGUAGE: str = 'en'
    PRIMARY_LANGUAGE: str = 'en'

    model_config = SettingsConfigDict(env_file=".env")  # ✅ pydantic v2 way

@lru_cache()  # ✅ cache so .env is only read once
def get_settings() -> Settings:
    return Settings()
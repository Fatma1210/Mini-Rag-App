from pydantic_settings import BaseSettings, SettingsConfigDict



class settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    class Config:
        env_file = ".env"


def get_settings():
    return settings()    
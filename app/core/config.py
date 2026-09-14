from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    secret_key: str = "dev-secret-key-change-me"
    database_url: str = "postgresql+psycopg://autopecas:autopecas@localhost:5432/autopecas"
    cors_origin_regex: str = r"^http://localhost(:\d+)?$"

    @property
    def is_testing(self) -> bool:
        return self.app_env == "test"


@lru_cache
def get_settings() -> Settings:
    return Settings()

"""Конфигурация приложения: читает значения из переменных окружения.

Используется всеми сервисами (ML API, Web). Секреты не хранятся в коде —
только в окружении или .env-файле (который не попадает в репозиторий).
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Все настройки проекта в одном месте."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # PostgreSQL
    postgres_user: str = "review_user"
    postgres_password: str = "change_me"
    postgres_db: str = "review_db"
    postgres_host: str = "db"
    postgres_port: int = 5432

    # ML API
    ml_api_host: str = "fastapi"
    ml_api_port: int = 8000

    # Flask
    flask_secret_key: str = "change_me"
    flask_port: int = 5000

    @property
    def async_database_url(self) -> str:
        """URL для async-подключения (FastAPI + asyncpg)."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def sync_database_url(self) -> str:
        """URL для синхронного подключения (Flask + psycopg2, Alembic)."""
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def ml_api_base_url(self) -> str:
        """Базовый URL ML API для запросов из Flask."""
        return f"http://{self.ml_api_host}:{self.ml_api_port}"


@lru_cache
def get_settings() -> Settings:
    """Возвращает единственный экземпляр настроек (кэшируется)."""
    return Settings()

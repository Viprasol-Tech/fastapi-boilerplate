"""Part of FastAPI Boilerplate by Viprasol Tech Private Limited (https://viprasol.com).

Application configuration backed by ``pydantic-settings``.

Settings are loaded from environment variables (optionally an ``.env`` file)
and exposed as a cached singleton via :func:`get_settings`.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application settings."""

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="FastAPI Boilerplate")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)

    api_v1_prefix: str = Field(default="/api/v1")

    # Comma-separated API keys accepted by the auth dependency.
    api_keys: str = Field(default="dev-secret-key")

    # Comma-separated list of allowed CORS origins ("*" allows all).
    cors_origins: str = Field(default="*")

    # Pagination defaults.
    default_page_size: int = Field(default=20, ge=1, le=100)
    max_page_size: int = Field(default=100, ge=1, le=1000)

    @property
    def allowed_api_keys(self) -> set[str]:
        """Return the configured API keys as a set."""
        return {key.strip() for key in self.api_keys.split(",") if key.strip()}

    @property
    def allowed_cors_origins(self) -> list[str]:
        """Return the configured CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance."""
    return Settings()

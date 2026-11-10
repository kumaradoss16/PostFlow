"""Runtime configuration for PostFlow local backend."""

from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings enforcing loopback-only binding invariants."""

    model_config = SettingsConfigDict(
        env_prefix="POSTFLOW_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "PostFlow Backend"
    version: str = "0.1.0"
    environment: Literal["development", "test", "production"] = "development"

    # Enforce loopback binding: only 127.0.0.1 is permitted
    host: str = Field(default="127.0.0.1", description="IPv4 loopback listener address")
    port: int = Field(
        default=0,
        ge=0,
        le=65535,
        description="Bound port (0 indicates ephemeral OS allocation)",
    )
    log_level: str = Field(default="INFO", description="Standard logging level")

    @field_validator("host")
    @classmethod
    def validate_loopback_only(cls, v: str) -> str:
        """Fail closed if any non-loopback host is configured."""
        if v.strip() != "127.0.0.1":
            raise ValueError(
                f"Security violation: PostFlow must bind only to '127.0.0.1', got '{v}'."
            )
        return v.strip()


def get_settings() -> Settings:
    """Retrieve application settings instance."""
    return Settings()

"""Project Configs."""

import logging
import os
import warnings
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class DataBaseConfig(BaseSettings):
    """Database config."""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        extra="allow",
    )
    PRODUCTION_DB: Optional[PostgresDsn] = None  # noqa: FA100
    DEVELOPMENT_DB: Optional[str] = None  # noqa: FA100
    DEVELOPMENT_MODE: bool = True
    DATABASE_URL: Optional[str] = None  # noqa: FA100

    @property
    def database_url(self) -> str:
        """Get the database URL from the environment variables."""
        if self.DEVELOPMENT_MODE:
            database_filename = "database.db"
            if url := self.DEVELOPMENT_DB:
                if not url:
                    url = f"sqlite:///src/models/{database_filename}"

                database_url = url
            else:
                error_message = "DEVELOPMENT_DB not set in environment variables."
                database_url = f"sqlite:///src/models/{database_filename}"
                warnings.warn(
                    f"{error_message} Using default URL: {database_url}",
                    stacklevel=2,
                )
        else:
            database_url = os.getenv("PRODUCTION_DB", "")
            if not database_url:
                error_message = (
                    "PRODUCTION_DB not set in env. DEVELOPMENT_MODE is False."
                )
                raise ValueError(error_message)
        return database_url


class Settings(BaseSettings):
    """App config."""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        extra="allow",
    )

    DATABASE: DataBaseConfig = Field(default_factory=DataBaseConfig)
    AT_USERNAME: str
    AT_API_KEY: str
    AT_SENDER_ID: Optional[str] = Field(default="16038")
    ZENOPAY_API_KEY: str

    @property
    def logger(self):
        """Get the logger."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        return logger


settings = Settings()


___all__ = ("settings",)

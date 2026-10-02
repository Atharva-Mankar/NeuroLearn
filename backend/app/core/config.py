"""Application configuration."""

from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings."""

    # Database configuration
    database_url: str = "sqlite:///./neurolearn.db"

    # Application info
    project_name: str = "NeuroLearn"
    version: str = "0.1.0"


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
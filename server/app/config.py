from pydantic_settings import BaseSettings
from typing import List
import json
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Data Configuration
    data_path: str = "../data"
    geotiff_cache_size: int = 100

    # CORS Configuration
    cors_origins: List[str] = ["http://localhost:3000", "https://victorious-forest-09f551a0f.1.azurestaticapps.net"]

    # API Configuration
    api_prefix: str = "/api"
    api_version: str = "v1"

    class Config:
        env_file = None  # Disable .env file loading temporarily
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Handle CORS origins from environment variable manually
        cors_env = os.getenv("CORS_ORIGINS")
        if cors_env:
            try:
                # Try to parse as JSON first
                self.cors_origins = json.loads(cors_env)
            except json.JSONDecodeError:
                # If not JSON, treat as comma-separated string
                self.cors_origins = [
                    origin.strip() for origin in cors_env.split(",") if origin.strip()
                ]


# Global settings instance
settings = Settings()

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Data Configuration
    data_path: str = "./data"
    geotiff_cache_size: int = 100

    # CORS Configuration
    cors_origins: List[str] = ["http://localhost:3000"]

    # API Configuration
    api_prefix: str = "/api"
    api_version: str = "v1"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

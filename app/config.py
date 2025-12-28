import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Browser
    browser_headless: bool = True
    browser_timeout: int = 30000
    max_concurrent: int = 5

    # Screenshot defaults
    default_width: int = 1280
    default_height: int = 720
    default_format: str = "png"
    default_quality: int = 80

    # Storage
    output_dir: Path = Path("/tmp/snapsht-screenshots")

    # Auth (optional)
    api_key: str | None = None

    # MySQL (for testing)
    mysql_host: str = "localhost"
    mysql_user: str = "root"
    mysql_password: str = ""
    mysql_database: str = "companies"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()

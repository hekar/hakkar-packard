from pathlib import Path
from typing import Optional, Literal

from pydantic import Field, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # Database settings
    database_url: str = Field(
        default="sqlite:///metrum.db",
        description="Database URL for SQLite"
    )
    
    # HTTP Client settings
    http_timeout: float = Field(
        default=30.0,
        description="HTTP client timeout in seconds"
    )
    base_url: Optional[str] = Field(
        default=None,
        description="Base URL for HTTP requests"
    )
    
    # WebSocket settings
    ws_url: Optional[str] = Field(
        default=None,
        description="WebSocket server URL"
    )
    ws_ping_interval: float = Field(
        default=20.0,
        description="WebSocket ping interval in seconds"
    )

    # PostgreSQL Log settings
    log_mode: Literal["filesystem", "csvlog", "syslog"] = Field(
        default="filesystem",
        description="PostgreSQL logging mode"
    )
    logs_dir: DirectoryPath = Field(
        default=Path("/workspaces/postgres-project/logs"),
        description="Directory containing PostgreSQL log files"
    )
    log_pattern: str = Field(
        default="postgresql-*.log",
        description="Pattern to match log files"
    )
    
    model_config = SettingsConfigDict(
        env_prefix="METRUM_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings() 
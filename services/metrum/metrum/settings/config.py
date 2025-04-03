from pathlib import Path
from typing import Optional, Literal

from pydantic import Field, DirectoryPath, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from metrum.common.logger import logger


class Settings(BaseSettings):
    """Application settings."""
    
    # Database settings
    database_url: str = Field(
        default="sqlite:///metrum.db",
        description="Database URL for SQLite"
    )
    
    # HTTP Client settings
    http_endpoint: str = Field(
        description="HTTP endpoint to send events to"
    )
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
        default=Path("../../data/customer-db/log"),
        description="Directory containing PostgreSQL log files"
    )
    log_pattern: str = Field(
        default="postgresql-*.log",
        description="Pattern to match log files"
    )
    poll_interval: float = Field(
        default=1.0,
        description="Interval between log file checks in seconds"
    )

    # Pattern configuration
    patterns_source: Optional[str] = Field(
        default=None,
        description="URL or file path to load patterns from. If not set, default patterns will be used."
    )
    patterns_cache_dir: Path = Field(
        default=Path("~/.cache/metrum"),
        description="Directory to cache pattern configurations downloaded from URLs"
    )
    patterns_cache_ttl: int = Field(
        default=3600,
        description="Time in seconds to cache pattern configurations before redownloading"
    )
    
    model_config = SettingsConfigDict(
        env_prefix="METRUM_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.debug("creating cache folder...", patterns_cache_dir=self.patterns_cache_dir)
        self.patterns_cache_dir = Path(self.patterns_cache_dir).expanduser()
        self.patterns_cache_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("created cache folder.", patterns_cache_dir=self.patterns_cache_dir)
        
        # Log all settings for debugging
        logger.debug(
            "initialized_settings",
            http_endpoint=self.http_endpoint,
            http_timeout=self.http_timeout,
            base_url=self.base_url,
            ws_url=self.ws_url,
            ws_ping_interval=self.ws_ping_interval,
            log_mode=self.log_mode,
            logs_dir=str(self.logs_dir),
            log_pattern=self.log_pattern,
            poll_interval=self.poll_interval,
            patterns_source=self.patterns_source,
            patterns_cache_dir=str(self.patterns_cache_dir),
            patterns_cache_ttl=self.patterns_cache_ttl
        )

settings = Settings()
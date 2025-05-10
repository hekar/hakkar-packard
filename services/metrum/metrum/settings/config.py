from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from metrum.common.logger import logger

class ModelConfig(BaseModel):
    """Model configuration settings."""
    env_file: str = Field(default=".env", description="Path to environment file")
    env_file_encoding: str = Field(default="utf-8", description="Environment file encoding")
    case_sensitive: bool = Field(default=True, description="Case sensitive environment variables")

class Settings(BaseSettings):
    """Application settings."""
    
    # Database settings
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/metrum",
        description="Database URL for PostgreSQL",
        env="METRUM_DATABASE_URL"
    )
    
    # Log monitor settings
    log_monitor_poll_interval: float = Field(
        default=1.0,
        description="Interval between log file checks in seconds",
        env="METRUM_LOG_MONITOR_POLL_INTERVAL"
    )
    log_monitor_http_endpoint: str = Field(
        default="http://localhost:8000/api/events",
        description="HTTP endpoint to send events to",
        env="METRUM_LOG_MONITOR_HTTP_ENDPOINT"
    )
    log_monitor_patterns_file: str = Field(
        default="metrum/config/patterns.json",
        description="Path to patterns configuration file",
        env="METRUM_LOG_MONITOR_PATTERNS_FILE"
    )

    # Metric sink settings
    metric_sink_type: str = Field(
        default="debug",
        description="Type of metric sink (options: http, debug, sqlite)",
        env="METRUM_METRIC_SINK_TYPE"
    )
    metric_sink_endpoint: str = Field(
        default="http://localhost:8000/api/metrics",
        description="HTTP endpoint for metric sink",
        env="METRUM_METRIC_SINK_ENDPOINT"
    )
    metric_sink_api_key: str | None = Field(
        default=None,
        description="API key for metric sink authentication",
        env="METRUM_METRIC_SINK_API_KEY"
    )
    metric_sink_db_path: str = Field(
        default="metrics.db",
        description="Database path for SQLite metric sink",
        env="METRUM_METRIC_SINK_DB_PATH"
    )
    metric_sink_pretty: bool = Field(
        default=True,
        description="Whether to format metric output in a pretty way",
        env="METRUM_METRIC_SINK_PRETTY"
    )
    
    # HTTP Client settings
    http_endpoint: str = Field(
        default="http://localhost:8000",
        description="HTTP endpoint to send events to",
        env="METRUM_HTTP_ENDPOINT"
    )
    http_timeout: int = Field(
        default=30,
        description="HTTP client timeout in seconds",
        env="METRUM_HTTP_TIMEOUT"
    )
    base_url: str = Field(
        default="http://localhost:8000",
        description="Base URL for HTTP requests",
        env="METRUM_BASE_URL"
    )
    
    # WebSocket settings
    ws_url: str = Field(
        default="ws://localhost:8000/ws",
        description="WebSocket server URL",
        env="METRUM_WS_URL"
    )
    ws_ping_interval: int = Field(
        default=30,
        description="WebSocket ping interval in seconds",
        env="METRUM_WS_PING_INTERVAL"
    )

    # PostgreSQL Log settings
    log_mode: str = Field(
        default="file",
        description="PostgreSQL logging mode",
        env="METRUM_LOG_MODE"
    )
    logs_dir: Path = Field(
        default=Path("logs").absolute(),
        description="Directory containing PostgreSQL log files",
        env="METRUM_LOGS_DIR"
    )
    log_pattern: str = Field(
        default="*.log",
        description="Pattern to match log files",
        env="METRUM_LOG_PATTERN"
    )
    poll_interval: int = Field(
        default=1,
        description="Interval between log file checks in seconds",
        env="METRUM_POLL_INTERVAL"
    )

    # Pattern configuration
    patterns_source: str = Field(
        default="file",
        description="Pattern source (file or database)",
        env="METRUM_PATTERNS_SOURCE"
    )
    patterns_cache_dir: Path = Field(
        default=Path("patterns_cache"),
        description="Directory to cache pattern configurations downloaded from URLs",
        env="METRUM_PATTERNS_CACHE_DIR"
    )
    patterns_cache_ttl: int = Field(
        default=3600,
        description="Time in seconds to cache pattern configurations before redownloading",
        env="METRUM_PATTERNS_CACHE_TTL"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.debug("creating cache folder...", patterns_cache_dir=self.patterns_cache_dir)
        self.patterns_cache_dir = Path(self.patterns_cache_dir).expanduser()
        self.patterns_cache_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("created cache folder.", patterns_cache_dir=self.patterns_cache_dir)
        
        # Log all settings for debugging
        logger.info(
            "initialized_settings",
            database_url=self.database_url,
            log_monitor_poll_interval=self.log_monitor_poll_interval,
            log_monitor_http_endpoint=self.log_monitor_http_endpoint,
            log_monitor_patterns_file=self.log_monitor_patterns_file,
            metric_sink_type=self.metric_sink_type,
            metric_sink_endpoint=self.metric_sink_endpoint,
            metric_sink_api_key=self.metric_sink_api_key,
            metric_sink_db_path=self.metric_sink_db_path,
            metric_sink_pretty=self.metric_sink_pretty,
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

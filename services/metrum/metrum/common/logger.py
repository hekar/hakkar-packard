import logging
import structlog
import os
from typing import Any

def configure_logger() -> None:
    """Configure structlog with standard processors and settings.
    
    The log level can be set using the LOG_LEVEL environment variable.
    Valid values are: DEBUG, INFO, WARNING, ERROR, CRITICAL
    Defaults to INFO if not set or invalid.
    """
    # Get log level from environment variable
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if log_level not in valid_levels:
        log_level = "INFO"
    

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,  # Add level filtering
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        cache_logger_on_first_use=True,
    )

# Configure the logger when this module is imported
configure_logger()

# Create a logger instance
logger = structlog.get_logger()

__all__ = ["logger"] 
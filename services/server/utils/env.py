import os
from typing import Optional, List, Any, Dict, Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file at module import time
load_dotenv()


# Custom exception for environment variable errors
class EnvironmentVariableError(Exception):
    def __init__(self, variable_name: str):
        self.variable_name = variable_name
        super().__init__(f"Environment variable {variable_name} is not set")


# Environment class to handle environment variables
class Environment:
    """
    Environment manager for handling environment variables with fallbacks.
    Functions as a singleton to ensure consistent configuration across the application.
    """

    _instance = None

    def __new__(cls) -> "Environment":
        """Singleton implementation to ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize with default values
            cls._instance._init_defaults()
        return cls._instance

    def _init_defaults(self) -> None:
        """Initialize default values for environment variables."""
        # Set default database URL if not specified
        default_db_url = "postgresql://postgres:postgres@localhost:5432/aifoundation"
        self.database_url = os.environ.get("DATABASE_URL", default_db_url)

        # Server settings
        self.port = self._get_int("PORT")
        self.host = os.environ.get("HOST", "0.0.0.0")
        self.debug = self._get_bool("DEBUG", False)

        # CORS settings
        default_cors = ["http://localhost:5173", "http://localhost:3000", "*"]
        self.cors_origins = os.environ.get(
            "CORS_ORIGINS", ",".join(default_cors)
        ).split(",")

        # Set dbmate environment variables if not already set
        if not os.getenv("DBMATE_SCHEMA_FILE"):
            os.environ["DBMATE_SCHEMA_FILE"] = os.getenv("SCHEMA_FILE", "db/schema.sql")

        if not os.getenv("DBMATE_MIGRATIONS_DIR"):
            os.environ["DBMATE_MIGRATIONS_DIR"] = os.getenv(
                "MIGRATIONS_DIR", "db/migrations"
            )

    def _get_int(self, name: str, default: int) -> int:
        """Get an environment variable as an integer with a default value."""
        value = os.environ.get(name)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default

    def _get_bool(self, name: str, default: bool) -> bool:
        """Get an environment variable as a boolean with a default value."""
        value = os.environ.get(name)
        if value is None:
            return default
        return value.lower() in ("yes", "true", "t", "1", "y")


def get_env_variable(name: str, default: Optional[str] = None) -> str:
    """
    Get an environment variable value.

    Args:
        name: Name of the environment variable
        default: Optional default value if environment variable is not set

    Returns:
        str: Value of the environment variable

    Raises:
        EnvironmentVariableError: If the environment variable is not set and no default is provided
    """
    value = os.getenv(name)
    if value is None:
        if default is not None:
            return default
        raise EnvironmentVariableError(name)
    return value


def get_int_env_variable(name: str, default: Optional[int] = None) -> int:
    """Get an environment variable as an integer."""
    value = os.getenv(name)
    if value is None:
        if default is not None:
            return default
        raise EnvironmentVariableError(name)
    try:
        return int(value)
    except ValueError:
        raise ValueError(f"Environment variable {name} must be an integer")


def get_bool_env_variable(name: str, default: Optional[bool] = None) -> bool:
    """Get an environment variable as a boolean."""
    value = os.getenv(name)
    if value is None:
        if default is not None:
            return default
        raise EnvironmentVariableError(name)

    return value.lower() in ("yes", "true", "t", "1")


def get_list_env_variable(
    name: str, separator: str = ",", default: Optional[List[str]] = None
) -> List[str]:
    """Get an environment variable as a list of strings."""
    value = os.getenv(name)
    if value is None:
        if default is not None:
            return default
        raise EnvironmentVariableError(name)

    return [item.strip() for item in value.split(separator) if item.strip()]


class EnvConfig(BaseModel):
    """Environment configuration model"""

    # Database settings
    database_url: str = Field(
        default_factory=lambda: get_env_variable(
            "DATABASE_URL",
            default="postgresql://postgres:postgres@localhost:5432/aifoundation",
        )
    )

    # Server settings
    port: int = Field(default_factory=lambda: get_int_env_variable("PORT", 8000))
    host: str = Field(default_factory=lambda: get_env_variable("HOST", "0.0.0.0"))
    debug: bool = Field(default_factory=lambda: get_bool_env_variable("DEBUG", False))

    # CORS settings
    cors_origins: List[str] = Field(
        default_factory=lambda: get_list_env_variable(
            "CORS_ORIGINS",
            default=["http://localhost:5173", "http://localhost:3000", "*"],
        )
    )

    # Migration settings
    migrations_dir: str = Field(
        default_factory=lambda: get_env_variable("MIGRATIONS_DIR", "db/migrations")
    )
    schema_file: str = Field(
        default_factory=lambda: get_env_variable("SCHEMA_FILE", "db/schema.sql")
    )


# Initialize environment configuration
# We keep both implementations for compatibility
env = EnvConfig()

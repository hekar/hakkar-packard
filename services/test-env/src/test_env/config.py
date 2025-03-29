from typing import Literal
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database connection settings."""

    model_config = SettingsConfigDict(env_prefix="TEST_ENV_DB_")

    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5433, description="Database port")
    user: str = Field(default="postgres", description="Database user")
    password: str = Field(default="postgres", description="Database password")
    database: str = Field(default="postgres", description="Database name")
    min_connections: int = Field(
        default=1, description="Minimum number of connections in the pool"
    )
    max_connections: int = Field(
        default=10, description="Maximum number of connections in the pool"
    )

    @property
    def connection_url(self) -> str:
        """Get the database connection URL."""
        return f"postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class DataGenerationSettings(BaseModel):
    """Settings for data generation."""

    num_customers: int = Field(
        default=10000, description="Number of customers to generate"
    )
    num_market_data: int = Field(
        default=100000, description="Number of market data points to generate"
    )
    accounts_per_customer: tuple[int, int] = Field(
        default=(2, 4), description="Range of accounts per customer (min, max)"
    )
    transactions_per_account: tuple[int, int] = Field(
        default=(10, 30), description="Range of transactions per account (min, max)"
    )
    investments_per_account: tuple[int, int] = Field(
        default=(1, 2),
        description="Range of investments per investment account (min, max)",
    )


class UISettings(BaseSettings):
    """Streamlit UI settings."""

    model_config = SettingsConfigDict(env_prefix="TEST_ENV_UI_")

    host: str = Field(default="0.0.0.0", description="UI host")
    port: int = Field(default=8501, description="UI port")


class SchemaSettings(BaseSettings):
    """Schema and query file settings."""

    model_config = SettingsConfigDict(env_prefix="TEST_ENV_")

    schema_file: str = Field(
        default="schema/financial_schema.sql", description="Path to the schema SQL file"
    )
    benchmark_queries_file: str = Field(
        default="schema/benchmark_queries.sql",
        description="Path to the benchmark queries SQL file",
    )


class AppSettings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_prefix="TEST_ENV_")

    debug: bool = Field(default=True, description="Debug mode")
    environment: Literal["development", "production", "testing"] = Field(
        default="development", description="Application environment"
    )
    app_version: str = Field(default="1.0.0", description="Application version")


class Settings(BaseSettings):
    """Global settings container."""

    model_config = SettingsConfigDict(env_prefix="TEST_ENV_")

    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    data_generation: DataGenerationSettings = Field(
        default_factory=DataGenerationSettings
    )
    ui: UISettings = Field(default_factory=UISettings)
    schem: SchemaSettings = Field(default_factory=SchemaSettings)
    app: AppSettings = Field(default_factory=AppSettings)


# Global settings instance
settings = Settings()

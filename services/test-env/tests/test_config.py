from test_env.config import settings


def test_database_settings():
    """Test database settings configuration."""
    assert settings.db.host == "localhost"
    assert settings.db.port == 5433
    assert settings.db.user == "postgres"
    assert settings.db.password == "postgres"
    assert settings.db.database == "postgres"
    assert settings.db.min_connections == 1
    assert settings.db.max_connections == 10

    # Test connection URL
    expected_url = "postgres://postgres:postgres@localhost:5433/postgres"
    assert settings.db.connection_url == expected_url


def test_data_generation_settings():
    """Test data generation settings configuration."""
    assert settings.data_generation.num_customers == 10000
    assert settings.data_generation.num_market_data == 100000
    assert settings.data_generation.accounts_per_customer == (2, 4)
    assert settings.data_generation.transactions_per_account == (10, 30)
    assert settings.data_generation.investments_per_account == (1, 2)


def test_ui_settings():
    """Test UI settings configuration."""
    assert settings.ui.host == "0.0.0.0"
    assert settings.ui.port == 8501


def test_schema_settings():
    """Test schema settings configuration."""
    assert settings.schem.schema_file == "schema/financial_schema.sql"
    assert settings.schem.benchmark_queries_file == "schema/benchmark_queries.sql"


def test_app_settings():
    """Test application settings configuration."""
    assert settings.app.debug is True
    assert settings.app.environment == "testing"
    assert settings.app.app_version == "1.0.0"

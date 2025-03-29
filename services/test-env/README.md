# test-env

A CLI application with Streamlit interface for test database management.

## Installation

This project uses Poetry for dependency management. To install:

```bash
# Install dependencies
poetry install
```

## Usage

After installation, you can use the CLI command:

```bash
poetry run test-env
```

Or run the Streamlit UI:

```bash
make run-ui
```

Or run tests:

```bash
make test
```

## Configuration

The application can be configured using environment variables:

### Database Settings (prefix: TEST_ENV_DB_)
- `TEST_ENV_DB_HOST`: Database host (default: "localhost")
- `TEST_ENV_DB_PORT`: Database port (default: 5433)
- `TEST_ENV_DB_USER`: Database user (default: "postgres")
- `TEST_ENV_DB_PASSWORD`: Database password (default: "postgres")
- `TEST_ENV_DB_DATABASE`: Database name (default: "postgres")
- `TEST_ENV_DB_MIN_CONNECTIONS`: Minimum pool connections (default: 1)
- `TEST_ENV_DB_MAX_CONNECTIONS`: Maximum pool connections (default: 10)


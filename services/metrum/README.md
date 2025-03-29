# Metrum Service

A CLI tool with HTTP and WebSocket client capabilities and PostgreSQL log reading.

## Requirements

- Python 3.9+
- Poetry
- dbmate (for database migrations)

## Installation

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

## Configuration

The service can be configured using environment variables or a `.env` file:

- `METRUM_DATABASE_URL`: SQLite database URL (default: `sqlite:///metrum.db`)
- `METRUM_BASE_URL`: Base URL for HTTP requests
- `METRUM_HTTP_TIMEOUT`: HTTP client timeout in seconds (default: 30.0)
- `METRUM_WS_URL`: WebSocket server URL
- `METRUM_WS_PING_INTERVAL`: WebSocket ping interval in seconds (default: 20.0)
- `METRUM_LOG_MODE`: PostgreSQL logging mode (default: `filesystem`)
- `METRUM_LOGS_DIR`: Directory containing PostgreSQL log files (default: `/workspaces/postgres-project/logs`)
- `METRUM_LOG_PATTERN`: Pattern to match log files (default: `postgresql-*.log`)

## Usage

### Initialize the Service

```bash
make metrum-init
# or
poetry run metrum init
```

This will:
- Create necessary directories (including logs directory)
- Initialize the SQLite database
- Create a default `.env` file if it doesn't exist
- Set up dbmate for migrations

### Run the Service

```bash
make metrum-run
# or
poetry run metrum run
```

### Reading PostgreSQL Logs

List available log files:
```bash
poetry run metrum logs list
```

Read logs:
```bash
# Read all logs
poetry run metrum logs read

# Follow logs in real-time
poetry run metrum logs read --follow

# Read logs since a specific time
poetry run metrum logs read --since "2024-03-28 00:00:00"

# Read logs between two timestamps
poetry run metrum logs read --since "2024-03-28 00:00:00" --until "2024-03-28 23:59:59"
```

## Development

The project uses:
- `poetry` for dependency management
- `pydantic` for settings management
- `click` for CLI interface
- `httpx` for HTTP client
- `websockets` for WebSocket client
- `sqlalchemy` for database ORM
- `dbmate` for database migrations

### Project Structure

```
metrum/
├── metrum/
│   ├── __init__.py
│   ├── cli.py         # CLI commands
│   ├── settings.py    # Configuration management
│   ├── db.py         # Database setup
│   ├── logs.py       # PostgreSQL log reader
│   └── clients.py    # HTTP and WebSocket clients
├── pyproject.toml    # Poetry configuration
└── README.md        # This file
``` 
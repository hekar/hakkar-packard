# Simple FastAPI Server

A minimal FastAPI server with a health endpoint for monitoring.

## Features

- Health check endpoint
- Versioned API routes
- CORS support
- Structured project layout

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry (dependency management)

### Installation

1. Install dependencies:

```bash
cd server
poetry install
```

2. Run the server:

```bash
poetry run python -m server.main
```

Or directly with uvicorn:

```bash
poetry run uvicorn server.main:app --reload
```

### API Endpoints

- `GET /`: Root endpoint with welcome message
- `GET /api/v1/health`: Health check endpoint

## Development

The server structure follows a modular approach:

```
server/
├── __init__.py
├── main.py            # Application entry point
├── routes/            # API routes
│   ├── __init__.py
│   ├── route_handler.py
│   └── v1/            # API version 1
│       ├── __init__.py
│       ├── health.py  # Health endpoint
│       └── v1.py      # V1 router
└── pyproject.toml     # Dependencies and project metadata
```

### Adding New Endpoints

To add new endpoints, create a new router module in the `routes/v1/` directory
and include it in the `routes/v1/v1.py` file.
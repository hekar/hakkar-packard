.PHONY: help build test run clean venv install dev-install lint format migrate-db populate-db bench-db run-dev run-ui

# Default target
help:
	@echo "Available commands:"
	@echo "  make help          - Show this help message"
	@echo "  make build        - Build the project"
	@echo "  make test         - Run tests"
	@echo "  make run          - Run the CLI application"
	@echo "  make run-dev      - Run the CLI application in development mode"
	@echo "  make run-ui       - Run the Streamlit UI for database management"
	@echo "  make venv         - Create virtual environment"
	@echo "  make install      - Install the package"
	@echo "  make dev-install  - Install development dependencies"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make migrate-db   - Create database schema"
	@echo "  make populate-db  - Populate database with test data"
	@echo "  make bench-db     - Run database benchmarks"

# Project setup
venv:
	poetry env use python3
	@echo "Virtual environment created. Activate with: poetry shell"

install:
	poetry install

dev-install:
	poetry install --with dev

# Build and test
build:
	poetry build

test:
	poetry run pytest tests/ -v

run:
	poetry run python -m test_env --help

run-ui:
	@echo "Starting Streamlit UI..."
	poetry run streamlit run src/test_env/ui/app.py --server.port 8501

# Development tools
lint:
	poetry run ruff check .
	poetry run ruff format --check .

lint-fix:
	poetry run ruff check --fix .
	poetry run ruff format .

format:
	poetry run ruff format .

# Database commands
migrate-db:
	@echo "Creating database schema..."
	poetry run python3 src/test_env migrate-db

populate-db:
	@echo "Populating database with test data..."
	poetry run python3 src/test_env populate-db

bench-db:
	@echo "Running database benchmarks..."
	poetry run python3 src/test_env bench-db

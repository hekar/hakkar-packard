.PHONY: help build test run clean docker-up docker-down docker-logs docker-shell venv install dev-install lint format migrate-db populate-db bench-db run-dev

# Default target
help:
	@echo "Available commands:"
	@echo "  make help          - Show this help message"
	@echo "  make build        - Build the project"
	@echo "  make test         - Run tests"
	@echo "  make run          - Run the CLI application"
	@echo "  make run-dev      - Run the CLI application in development mode"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make venv         - Create virtual environment"
	@echo "  make install      - Install the package"
	@echo "  make dev-install  - Install development dependencies"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make docker-up    - Start PostgreSQL container in tmux"
	@echo "  make docker-down  - Stop PostgreSQL container"
	@echo "  make docker-logs  - View PostgreSQL logs"
	@echo "  make docker-shell - Open PostgreSQL shell"
	@echo "  make migrate-db   - Create database schema"
	@echo "  make populate-db  - Populate database with test data in tmux"
	@echo "  make bench-db     - Run database benchmarks"

# Project setup
venv:
	uv venv
	@echo "Virtual environment created. Activate with: source .venv/bin/activate"

install:
	uv pip install -e .

dev-install:
	uv pip install -e ".[dev]"

# Build and test
build:
	uv pip install build
	python -m build

test:
	pytest tests/ -v

run:
	uv run python test-env --help

# Development tools
lint:
	ruff check .
	ruff format --check .

format:
	ruff format .

# Docker commands
docker-up:
	tmux kill-session -t postgres 2>/dev/null || true
	tmux new-session -d -s postgres
	tmux send-keys -t postgres "docker-compose up" C-m

docker-down:
	docker-compose down
	tmux kill-session -t postgres 2>/dev/null || true

docker-logs:
	docker-compose logs -f postgres

docker-shell:
	docker-compose exec postgres psql -U postgres -d postgres

# Database commands
migrate-db:
	@echo "Creating database schema..."
	test-env migrate-db

populate-db:
	@echo "Populating database with test data..."
	tmux kill-session -t populate-db 2>/dev/null || true
	tmux new-session -d -s populate-db
	tmux send-keys -t populate-db "uv run python3 ./src/test_env populate-db" C-m

bench-db:
	@echo "Running database benchmarks..."
	test-env bench-db

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 
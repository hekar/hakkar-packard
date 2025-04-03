.PHONY: install test test-cov format lint lint-fix run clean db-up db-rollback db-reset

# Default target
all: install

# Install dependencies using Poetry
install:
	poetry install

# Run tests
test:
	poetry run pytest

# Run tests with coverage
test-cov:
	poetry run pytest --cov=metrum --cov-report=term-missing --cov-report=html

# Format code using black and isort
format:
	poetry run black .
	poetry run isort .

# Run the service
run:
	poetry run metrum run

# Clean up Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +

# Database migration commands
db-up:
	poetry run metrum db up

db-rollback:
	poetry run metrum db rollback

db-reset:
	poetry run metrum db reset

# Fix lint errors using ruff
lint-fix:
	poetry run ruff check --fix .

# Show help
help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make test-cov   - Run tests with coverage report"
	@echo "  make format     - Format code using black and isort"
	@echo "  make lint-fix   - Fix lint errors using ruff"
	@echo "  make run        - Run the service"
	@echo "  make clean      - Clean up Python cache files"
	@echo "  make db-up      - Upgrade database to latest version"
	@echo "  make db-rollback - Rollback database to first version"
	@echo "  make db-reset   - Reset database and run all migrations"
	@echo "  make help       - Show this help message" 
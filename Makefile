.PHONY: help migrate rollback migrate-new run-server run-ui metrum-init metrum-run

# Default target when just running 'make'
.DEFAULT_GOAL := help

# Include db .env file if it exists for database commands
ifneq (,$(wildcard ./services/db/.env))
include ./services/db/.env
export
endif

# Help target that lists all available commands
help: ## Show this help message
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@printf "\033[1;32mApplication Commands:\033[0m\n"
	@printf "  \033[1;36mrun-server\033[0m               Start the backend development server\n"
	@printf "  \033[1;36mrun-ui\033[0m                   Start the frontend development server\n"
	@printf "  \033[1;36mmetrum-init\033[0m             Initialize the Metrum service\n"
	@printf "  \033[1;36mmetrum-run\033[0m              Run the Metrum service\n"
	@echo ""
	@printf "\033[1;32mDatabase Commands:\033[0m\n"
	@printf "  \033[1;36mmigrate\033[0m                  Run database migrations\n"
	@printf "  \033[1;36mrollback\033[0m                 Rollback the last database migration\n"
	@printf "  \033[1;36mmigrate-new\033[0m              Create a new database migration (usage: make migrate-new name=migration_name)\n"
	@echo ""
	@printf "\033[1;32mHelp:\033[0m\n"
	@printf "  \033[1;36mhelp\033[0m                     Show this help message\n"

#-------------------------------------------------------
# Application Commands
#-------------------------------------------------------

run-server: ## Start the backend development server
	@echo "Starting backend server..."
	cd services/server && \
	poetry install --no-root && \
	poetry run python -m main

run-ui: ## Start the frontend development server
	@echo "Starting frontend server..."
	cd services/ui && \
	yarn install && \
	yarn dev --host 0.0.0.0

run-metrum: ## Run the Metrum service
	@echo "Running Metrum service..."
	cd services/metrum && \
	poetry run metrum run

#-------------------------------------------------------
# Database Commands
#-------------------------------------------------------

migrate: ## Run database migrations
	@echo "Running database migrations..."
	cd services && (eval $$(cat db/.env | sed 's/^/export /') && dbmate up)

rollback: ## Rollback the last database migration
	@echo "Rolling back the last database migration..."
	cd services && (eval $$(cat db/.env | sed 's/^/export /') && dbmate down)

migrate-new: ## Create a new database migration (usage: make migrate-new name=migration_name)
	@if [ -z "$(name)" ]; then \
		echo "Error: migration name is required. Usage: make migrate-new name=migration_name"; \
		exit 1; \
	fi
	@echo "Creating new migration: $(name)..."
	cd services && (eval $$(cat db/.env | sed 's/^/export /') && dbmate new $(name))

# Florence MCP Servers Makefile

.PHONY: help build up down logs test clean dev prod

# Default target
help:
	@echo "Florence MCP Servers - Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  make dev           - Start development environment"
	@echo "  make dev-with-tools - Start development with pgAdmin and Redis Commander"
	@echo "  make logs          - Show logs from all containers"
	@echo "  make logs-recipe   - Show logs from recipe API server only"
	@echo "  make test          - Run tests in Docker container"
	@echo "  make shell         - Get shell access to recipe API container"
	@echo ""
	@echo "Production:"
	@echo "  make prod          - Start production environment"
	@echo "  make prod-build    - Build and start production environment"
	@echo ""
	@echo "Management:"
	@echo "  make up            - Start all services"
	@echo "  make down          - Stop all services"
	@echo "  make build         - Build all Docker images"
	@echo "  make clean         - Remove all containers, volumes, and images"
	@echo "  make restart       - Restart all services"
	@echo ""
	@echo "Environment file should be created: cp .env.example .env"

# Development environment
dev:
	@echo "Starting development environment..."
	docker-compose up -d
	@echo "Recipe API Server is running. Check logs with: make logs"

dev-with-tools:
	@echo "Starting development environment with tools..."
	docker-compose --profile tools up -d
	@echo "Development tools available:"
	@echo "  - pgAdmin: http://localhost:8080 (admin@florence.local / admin)"
	@echo "  - Redis Commander: http://localhost:8081"

# Production environment
prod:
	@echo "Starting production environment..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-build:
	@echo "Building and starting production environment..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# Basic Docker operations
up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

restart:
	docker-compose restart

# Logging
logs:
	docker-compose logs -f

logs-recipe:
	docker-compose logs -f recipe-api-server

# Testing
test:
	@echo "Running tests in Docker container..."
	docker-compose exec recipe-api-server pytest
	
test-coverage:
	@echo "Running tests with coverage..."
	docker-compose exec recipe-api-server pytest --cov=src --cov-report=html

# Development utilities
shell:
	docker-compose exec recipe-api-server bash

shell-postgres:
	docker-compose exec postgres psql -U postgres -d sous_chef

shell-redis:
	docker-compose exec redis redis-cli

# Database operations
db-migrate:
	@echo "Running database migrations..."
	docker-compose exec recipe-api-server python -m alembic upgrade head

db-reset:
	@echo "Resetting database..."
	docker-compose down -v postgres
	docker-compose up -d postgres

# Cleanup operations
clean:
	@echo "Cleaning up all Docker resources..."
	docker-compose down -v --remove-orphans
	docker system prune -a --volumes -f

clean-images:
	@echo "Removing Florence Docker images..."
	docker images | grep florence | awk '{print $$3}' | xargs -r docker rmi -f

# Health checks
health:
	@echo "Checking service health..."
	docker-compose ps
	@echo ""
	@echo "Recipe API Server health:"
	docker-compose exec recipe-api-server python -c "print('✅ Recipe API Server is healthy')"

# Environment setup
setup:
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp .env.example .env; \
		echo "⚠️  Please edit .env file with your API keys"; \
	fi
	@echo "Building Docker images..."
	make build
	@echo "Starting services..."
	make dev
	@echo ""
	@echo "✅ Setup complete!"
	@echo "Next steps:"
	@echo "  1. Edit .env file with your Spoonacular API key"
	@echo "  2. Run 'make restart' to apply the changes"
	@echo "  3. Run 'make test' to verify everything works"

# Install pre-commit hooks (for development)
install-hooks:
	@echo "Installing pre-commit hooks..."
	pip install pre-commit
	pre-commit install
	@echo "✅ Pre-commit hooks installed"

# Format code
format:
	docker-compose exec recipe-api-server black src/ tests/
	docker-compose exec recipe-api-server isort src/ tests/

# Lint code
lint:
	docker-compose exec recipe-api-server flake8 src/ tests/
	docker-compose exec recipe-api-server mypy src/
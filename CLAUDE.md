# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server collection for building a personal sous chef ambient agent. Currently implements recipe search and management with plans for meal planning, inventory tracking, and food ordering.

> **📖 See [README.md](README.md) for user-facing documentation and complete roadmap**

## Current Implementation

**Status**: Active development - Recipe API Server implemented
**Architecture**: Docker-based microservices with MCP protocol
**Technology Stack**: Python 3.9+, MCP SDK, Docker Compose, PostgreSQL, Redis

### Implemented Features
- **Recipe API Server**: Full implementation with Spoonacular API integration
- **Shared Data Models**: Recipe, Ingredient, NutritionInfo classes
- **Docker Environment**: Complete dev/prod setup with PostgreSQL and Redis
- **Testing Infrastructure**: pytest with async support and coverage reporting

## Quick Start Commands

### Development Environment
```bash
# Setup and start everything
make setup          # Creates .env, builds images, starts services
make dev            # Start development environment  
make test           # Run all tests
make logs           # View all service logs

# Development with tools (pgAdmin, Redis Commander)
make dev-with-tools

# Individual operations
make shell          # Access recipe server container
make format         # Format code with black/isort
make lint           # Run flake8 and mypy
```

### Individual Server Development
```bash
cd servers/recipe_api_server
pip install -r requirements.txt
cp .env.example .env  # Edit with API keys
python src/main.py
pytest
```

## Repository Architecture

The project uses a microservices architecture with shared utilities:

```
florence-mcp-servers/
├── shared/                     # Common utilities and data models  
│   ├── types/                 # Recipe, Ingredient, NutritionInfo classes
│   ├── utils/                 # Logger setup and shared utilities
│   └── config/                # Shared configuration management
├── servers/                   # Individual MCP servers
│   └── recipe_api_server/     # Implemented: Recipe search & details
│       ├── src/
│       │   ├── main.py       # MCP server entry point
│       │   ├── tools/        # search_recipes, get_recipe_details  
│       │   └── services/     # spoonacular.py API integration
│       └── tests/            # Unit and integration tests
└── tests/                    # Cross-server integration tests
```

## MCP Server Architecture

### Recipe API Server (`servers/recipe_api_server/`)
**Tools Available:**
- `search_recipes`: Search by query, dietary restrictions, cuisine type, cooking time
- `get_recipe_details`: Get full recipe information by ID

**Implementation Pattern:**
- `src/main.py`: MCP server with stdio transport and tool registration
- `src/tools/`: Individual MCP tool implementations
- `src/services/`: External API clients (currently Spoonacular)
- `tests/`: Unit tests for tools and services

### Shared Data Models (`shared/types/recipe.py`)
- **Recipe**: Complete recipe with ingredients, instructions, nutrition, metadata
- **Ingredient**: Name, amount, unit, optional notes  
- **NutritionInfo**: Calories, macronutrients, fiber, sugar
- All models support dict serialization and scaling functionality

## Technology Stack

- **Python 3.9+** with asyncio for concurrent operations
- **MCP SDK** for Model Context Protocol implementation  
- **httpx** for async HTTP client operations
- **structlog** for structured logging
- **pytest + pytest-asyncio** for testing with async support
- **Docker Compose** for local development environment

## Environment Variables

### Recipe APIs (Active)
```bash
SPOONACULAR_API_KEY=your_spoonacular_api_key_here
EDAMAM_APP_ID=your_edamam_app_id_here  # Future use
EDAMAM_APP_KEY=your_edamam_app_key_here  # Future use
```

### Food Delivery APIs (Planned)
```bash
UBER_EATS_CLIENT_ID=your_uber_eats_client_id
UBER_EATS_CLIENT_SECRET=your_uber_eats_client_secret
```

### Infrastructure
```bash
# PostgreSQL (available but not yet used by recipe server)
POSTGRES_DB=sous_chef
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432

# Redis (available but not yet used)  
REDIS_PASSWORD=
REDIS_PORT=6379

# Application
LOG_LEVEL=INFO
ENVIRONMENT=development
```

## Testing

The project uses pytest with async support and multiple test markers:

```bash
# Run all tests
make test
pytest

# Run specific test types  
pytest -m "not integration"  # Unit tests only
pytest -m integration        # Integration tests only
pytest -m slow              # Slow tests only

# Run with coverage
make test-coverage
pytest --cov=src --cov-report=html
```

**Test Structure:**
- `servers/recipe_api_server/tests/`: Server-specific unit tests
- `tests/`: Cross-server integration tests  
- `pytest.ini`: Configures test discovery, markers, and async mode

## Development Workflow

### Adding New MCP Tools
1. Create tool implementation in `servers/{server}/src/tools/{tool_name}.py`
2. Register tool in `servers/{server}/src/main.py`
3. Add external service if needed in `servers/{server}/src/services/`
4. Write tests in `servers/{server}/tests/test_tools/`
5. Update tool documentation in server README

### Code Quality
```bash
make format     # Auto-format with black and isort
make lint       # Check with flake8 and mypy
```

**Standards:**
- All async functions properly handle timeouts and errors
- External API responses are validated against shared data models  
- Environment variables are validated on server startup
- All new features include corresponding tests

## Architecture Notes

- **MCP Protocol**: Uses stdio transport for LLM integration
- **Async First**: All I/O operations use async/await patterns
- **Shared Models**: All servers use common data structures from `shared/types/`
- **Container Ready**: Full Docker development and production environment
- **Testable**: External APIs mocked in tests, clear separation of concerns
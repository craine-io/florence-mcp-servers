# Recipe API MCP Server

**Part of the [Florence MCP Servers](../../README.md) collection** - the foundational server that provides recipe search, storage, and management capabilities using the Spoonacular API.

## 🏗️ Project Context

This is the **first implemented server** in the Florence MCP ecosystem, designed to be the cornerstone for building a personal sous chef ambient agent. The Recipe API Server handles all recipe-related operations and provides the foundation for future meal planning, inventory tracking, and food ordering servers.

**See the [main project README](../../README.md)** for the complete roadmap and multi-server architecture.

## Features

- **Recipe Search**: Search for recipes by query, dietary restrictions, and cuisine type
- **Recipe Details**: Get detailed information about specific recipes
- **Nutrition Analysis**: Extract nutrition information from recipes
- **Multiple APIs**: Currently supports Spoonacular (Edamam planned)

## Setup

### Option 1: Docker (Recommended)

> **💡 Quick Start**: For the complete Docker setup guide, see the [main project README](../../README.md#-quick-start-with-docker)

1. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your Spoonacular API key
   ```

2. **Get Spoonacular API Key**:
   - Sign up at [Spoonacular API](https://spoonacular.com/food-api)
   - Get your API key and add it to `.env`

3. **Run with Docker**:
   ```bash
   # Quick setup (from project root)
   make setup
   
   # Or manually
   docker-compose up -d
   ```

### Option 2: Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your Spoonacular API key
   ```

3. **Run the server**:
   ```bash
   python src/main.py
   ```

## Usage

### Running with Docker

```bash
# Start development environment
make dev

# View logs
make logs

# Run tests
make test

# Get shell access
make shell

# Stop services
make down
```

### Running Locally

```bash
python src/main.py
```

### Available Tools

#### `search_recipes`
Search for recipes with optional filters.

**Parameters**:
- `query` (required): Search query for recipes
- `dietary_restrictions` (optional): Array of dietary restrictions
- `cuisine_type` (optional): Type of cuisine
- `max_time` (optional): Maximum cooking time in minutes
- `number` (optional): Number of recipes to return (default: 10)

**Example**:
```json
{
  "query": "chicken pasta",
  "dietary_restrictions": ["vegetarian"],
  "cuisine_type": "italian",
  "max_time": 30,
  "number": 5
}
```

#### `get_recipe_details`
Get detailed information about a specific recipe.

**Parameters**:
- `recipe_id` (required): The unique identifier for the recipe

**Example**:
```json
{
  "recipe_id": "716429"
}
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_tools/test_search_recipes.py
```

## Development

### Code Quality

```bash
# Format code
black .
isort .

# Lint code
flake8 .

# Type checking
mypy .
```

## API Integration

### Spoonacular API

- **Base URL**: `https://api.spoonacular.com/recipes`
- **Authentication**: API key required
- **Rate Limits**: Check your plan limits
- **Documentation**: [Spoonacular API Docs](https://spoonacular.com/food-api/docs)

### Supported Dietary Restrictions

- vegetarian
- vegan
- glutenFree
- dairyFree
- ketogenic
- paleo
- primal
- whole30

### Supported Cuisines

- italian
- mexican
- chinese
- indian
- thai
- japanese
- french
- mediterranean
- american

## 🔗 Integration with Florence Ecosystem

### Current Role
- **Foundation Server**: Provides recipe data for all other planned servers
- **Standalone Capability**: Fully functional as an independent MCP server
- **Shared Data Models**: Uses common data structures from `shared/types/`

### Future Integrations
Once additional servers are implemented, the Recipe API Server will provide data to:
- **Meal Planning Server**: Recipe suggestions for weekly/monthly planning
- **Pantry Inventory Server**: Ingredient lists for shopping and inventory
- **Nutrition Tracking Server**: Nutritional data for meal analysis
- **Restaurant Delivery Server**: Recipe alternatives when ingredients unavailable

### Architecture Benefits
- **Microservice Design**: Independent deployment and scaling
- **Shared Infrastructure**: Common PostgreSQL and Redis services
- **Unified Data Models**: Consistent Recipe, Ingredient, and Nutrition types
- **Container Ready**: Docker-first development and deployment

For the complete Florence MCP Servers architecture and roadmap, see the [main project documentation](../../README.md).
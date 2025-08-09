# Claude Desktop Integration Guide

## Overview

The Florence Recipe MCP Server is now ready for integration with Claude Desktop. This guide will walk you through setting it up.

## Prerequisites

1. **Claude Desktop App**: Install from [Claude.ai](https://claude.ai/desktop)
2. **Python Environment**: Python 3.9+ with MCP dependencies
3. **Spoonacular API Key**: Get from [Spoonacular API](https://spoonacular.com/food-api)

## Installation Options

### Option 1: Docker-based Setup (Recommended)

1. **Build the Docker container**:
   ```bash
   docker-compose build recipe-api-server
   ```

2. **Create your Claude Desktop config** at `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "florence-recipe-server": {
         "command": "docker",
         "args": [
           "run", "--rm", "-i",
           "--env-file", "/absolute/path/to/florence-mcp-servers/.env",
           "florence-mcp-servers-recipe-api-server",
           "python", "src/main.py"
         ]
       }
     }
   }
   ```

3. **Set up your environment file** (`.env` in project root):
   ```bash
   SPOONACULAR_API_KEY=your_actual_api_key_here
   LOG_LEVEL=INFO
   ```

### Option 2: Direct Python Setup

1. **Install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   pip install -r servers/recipe_api_server/requirements.txt
   ```

2. **Create your Claude Desktop config**:
   ```json
   {
     "mcpServers": {
       "florence-recipe-server": {
         "command": "python",
         "args": [
           "/absolute/path/to/florence-mcp-servers/servers/recipe_api_server/src/main.py"
         ],
         "env": {
           "SPOONACULAR_API_KEY": "your_actual_api_key_here",
           "LOG_LEVEL": "INFO",
           "PYTHONPATH": "/absolute/path/to/florence-mcp-servers"
         }
       }
     }
   }
   ```

## Configuration Details

### Required Environment Variables
- `SPOONACULAR_API_KEY`: Your Spoonacular API key (required)
- `LOG_LEVEL`: Optional, defaults to "INFO"

### Important Notes
- **Use absolute paths** - Claude Desktop needs full paths to executables and scripts
- **Set PYTHONPATH** - Ensures the server can find shared modules
- **Verify paths** - Use `pwd` (macOS/Linux) or `cd` (Windows) to get absolute paths

## Available Tools

Once configured, you'll have access to these tools in Claude Desktop:

### 1. `search_recipes`
Search for recipes by query, dietary restrictions, and cuisine type.
- **Parameters**: `query` (required), `dietary_restrictions`, `cuisine_type`, `max_time`, `number`
- **Example**: "Search for vegetarian pasta recipes"

### 2. `get_recipe_details` 
Get detailed information about a specific recipe.
- **Parameters**: `recipe_id` (required)
- **Example**: After searching, get full details for a specific recipe

## Troubleshooting

### Check Claude Desktop Logs
```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

### Common Issues

1. **"Command not found"**: Ensure absolute paths in config
2. **"Permission denied"**: Check file permissions on scripts
3. **"Import errors"**: Verify PYTHONPATH is set correctly
4. **"No API results"**: Check your Spoonacular API key

### Test the Server Manually
```bash
# Option 1: Docker
docker-compose run --rm recipe-api-server python src/main.py

# Option 2: Direct Python
cd servers/recipe_api_server
python src/main.py
```

The server should start and show: "Starting Recipe API Server"

## Usage Examples

Once integrated with Claude Desktop, you can ask Claude:

- "Find me some healthy vegetarian dinner recipes"
- "Search for quick Italian pasta dishes under 30 minutes"  
- "Get the full recipe details for recipe ID 12345"
- "Show me gluten-free dessert recipes"

The MCP server will handle the API calls and return formatted recipe information directly in your Claude Desktop conversation.

## Security Notes

- Keep your API keys secure and never commit them to version control
- The MCP server only accesses the Spoonacular API for recipe data
- All communication with Claude Desktop is through secure stdio transport
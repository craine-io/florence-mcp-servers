import asyncio
import logging
import sys
import os
from contextlib import AsyncExitStack

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

# Import tools
from tools.search_recipes import search_recipes
from tools.get_recipe_details import get_recipe_details
from shared.utils import setup_logger

# Configure logging
logger = setup_logger("recipe-api-server", level=os.getenv("LOG_LEVEL", "INFO"))

# Initialize server
server = Server("recipe-api-server")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="search_recipes",
            description="Search for recipes by query, dietary restrictions, and cuisine type",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for recipes"
                    },
                    "dietary_restrictions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of dietary restrictions (e.g., vegetarian, gluten-free)"
                    },
                    "cuisine_type": {
                        "type": "string",
                        "description": "Type of cuisine (e.g., italian, mexican)"
                    },
                    "max_time": {
                        "type": "number",
                        "description": "Maximum cooking time in minutes"
                    },
                    "number": {
                        "type": "number",
                        "description": "Number of recipes to return (default: 10)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_recipe_details",
            description="Get detailed information about a specific recipe",
            inputSchema={
                "type": "object",
                "properties": {
                    "recipe_id": {
                        "type": "string",
                        "description": "The unique identifier for the recipe"
                    }
                },
                "required": ["recipe_id"]
            }
        ),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        logger.info(f"Calling tool: {name} with arguments: {arguments}")
        
        if name == "search_recipes":
            result = await search_recipes(**arguments)
        elif name == "get_recipe_details":
            result = await get_recipe_details(**arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
        
        logger.info(f"Tool {name} completed successfully")
        return [TextContent(type="text", text=str(result))]
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    """Run the server."""
    logger.info("Starting Recipe API Server")
    
    # Check for required environment variables
    if not os.getenv("SPOONACULAR_API_KEY"):
        logger.warning("SPOONACULAR_API_KEY not set. Recipe search may not work.")
    
    # Use stdin/stdout streams
    async with AsyncExitStack() as stack:
        streams = await stack.enter_async_context(stdio_server())
        await server.run(
            streams[0], streams[1], server.create_initialization_options()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server failed: {e}")
        sys.exit(1)
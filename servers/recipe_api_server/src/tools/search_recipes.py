import asyncio
from typing import Dict, List, Any, Optional
import logging
from services.spoonacular import SpoonacularService

logger = logging.getLogger(__name__)

async def search_recipes(
    query: str,
    dietary_restrictions: Optional[List[str]] = None,
    cuisine_type: Optional[str] = None,
    max_time: Optional[int] = None,
    number: int = 10
) -> Dict[str, Any]:
    """
    Search for recipes using Spoonacular API.
    
    Args:
        query: Search query for recipes
        dietary_restrictions: List of dietary restrictions (e.g., ["vegetarian", "gluten-free"])
        cuisine_type: Type of cuisine (e.g., "italian", "mexican")
        max_time: Maximum cooking time in minutes
        number: Number of recipes to return (default: 10)
    
    Returns:
        Dictionary containing search results and metadata
    """
    try:
        # Initialize service
        async with SpoonacularService() as spoonacular:
            result = await spoonacular.search_recipes(
                query=query,
                dietary_restrictions=dietary_restrictions,
                cuisine_type=cuisine_type,
                max_time=max_time,
                number=number
            )
            
            # Sort recipes by relevance to query
            sorted_recipes = _sort_by_relevance(result["recipes"], query)
            
            return {
                "recipes": sorted_recipes,
                "total_found": result["total_results"],
                "query": query,
                "filters_applied": {
                    "dietary_restrictions": dietary_restrictions,
                    "cuisine_type": cuisine_type,
                    "max_time": max_time
                },
                "source": result["source"]
            }
        
    except Exception as e:
        logger.error(f"Error searching recipes: {e}")
        return {
            "recipes": [],
            "total_found": 0,
            "query": query,
            "error": str(e),
            "filters_applied": {
                "dietary_restrictions": dietary_restrictions,
                "cuisine_type": cuisine_type,
                "max_time": max_time
            }
        }

def _sort_by_relevance(recipes: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """Sort recipes by relevance to search query."""
    query_words = set(query.lower().split())
    
    def relevance_score(recipe):
        title_words = set(recipe.get("title", "").lower().split())
        description_words = set(recipe.get("description", "").lower().split())
        
        title_matches = len(query_words.intersection(title_words))
        description_matches = len(query_words.intersection(description_words))
        
        return title_matches * 2 + description_matches
    
    return sorted(recipes, key=relevance_score, reverse=True)
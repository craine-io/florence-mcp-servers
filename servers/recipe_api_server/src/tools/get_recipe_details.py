from typing import Optional, Dict, Any
import logging
from services.spoonacular import SpoonacularService

logger = logging.getLogger(__name__)

async def get_recipe_details(recipe_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific recipe.
    
    Args:
        recipe_id: The unique identifier for the recipe
        
    Returns:
        Dictionary containing detailed recipe information
    """
    try:
        async with SpoonacularService() as spoonacular:
            recipe = await spoonacular.get_recipe_details(recipe_id)
            
            if recipe:
                return {
                    "recipe": recipe.to_dict(),
                    "found": True,
                    "source": "spoonacular"
                }
            else:
                return {
                    "recipe": None,
                    "found": False,
                    "error": f"Recipe with ID {recipe_id} not found",
                    "source": "spoonacular"
                }
    
    except Exception as e:
        logger.error(f"Error getting recipe details for {recipe_id}: {e}")
        return {
            "recipe": None,
            "found": False,
            "error": str(e),
            "source": "spoonacular"
        }
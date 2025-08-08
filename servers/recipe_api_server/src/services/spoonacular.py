import aiohttp
import asyncio
from typing import Dict, List, Any, Optional
import logging
import os
from shared.types import Recipe, Ingredient, NutritionInfo

logger = logging.getLogger(__name__)

class SpoonacularService:
    """Service for interacting with Spoonacular Recipe API."""
    
    def __init__(self):
        self.api_key = os.getenv("SPOONACULAR_API_KEY")
        self.base_url = "https://api.spoonacular.com/recipes"
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_recipes(
        self,
        query: str,
        dietary_restrictions: Optional[List[str]] = None,
        cuisine_type: Optional[str] = None,
        max_time: Optional[int] = None,
        number: int = 10
    ) -> Dict[str, Any]:
        """Search recipes using Spoonacular API."""
        if not self.api_key:
            raise ValueError("SPOONACULAR_API_KEY environment variable not set")
        
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        params = {
            "apiKey": self.api_key,
            "query": query,
            "number": number,
            "addRecipeInformation": True,
            "fillIngredients": True
        }
        
        if dietary_restrictions:
            params["diet"] = ",".join(dietary_restrictions)
        
        if cuisine_type:
            params["cuisine"] = cuisine_type
        
        if max_time:
            params["maxReadyTime"] = max_time
        
        try:
            async with self.session.get(
                f"{self.base_url}/complexSearch",
                params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                return {
                    "recipes": self._format_recipes(data.get("results", [])),
                    "total_results": data.get("totalResults", 0),
                    "source": "spoonacular"
                }
        
        except aiohttp.ClientError as e:
            logger.error(f"Spoonacular API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
    
    async def get_recipe_details(self, recipe_id: str) -> Optional[Recipe]:
        """Get detailed recipe information by ID."""
        if not self.api_key:
            raise ValueError("SPOONACULAR_API_KEY environment variable not set")
        
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        params = {
            "apiKey": self.api_key,
            "includeNutrition": True
        }
        
        try:
            async with self.session.get(
                f"{self.base_url}/{recipe_id}/information",
                params=params
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                return self._format_single_recipe(data)
        
        except aiohttp.ClientError as e:
            logger.error(f"Spoonacular API error for recipe {recipe_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def _format_recipes(self, raw_recipes: List[Dict]) -> List[Dict[str, Any]]:
        """Format raw Spoonacular recipe data."""
        formatted = []
        
        for recipe in raw_recipes:
            formatted.append({
                "id": str(recipe.get("id")),
                "title": recipe.get("title"),
                "description": recipe.get("summary", ""),
                "image_url": recipe.get("image"),
                "prep_time_minutes": recipe.get("preparationMinutes", 0),
                "cook_time_minutes": recipe.get("cookingMinutes", 0),
                "total_time_minutes": recipe.get("readyInMinutes", 0),
                "servings": recipe.get("servings", 1),
                "source_url": recipe.get("sourceUrl"),
                "cuisine_type": recipe.get("cuisines", []),
                "dietary_tags": recipe.get("diets", []),
                "ingredients": self._extract_ingredients(recipe.get("extendedIngredients", [])),
                "nutrition": self._extract_nutrition(recipe.get("nutrition", {})),
                "source": "spoonacular"
            })
        
        return formatted
    
    def _format_single_recipe(self, recipe_data: Dict) -> Recipe:
        """Format a single recipe from Spoonacular API into Recipe object."""
        ingredients = [
            Ingredient(
                name=ing.get("name", ""),
                amount=ing.get("amount", 0),
                unit=ing.get("unit", ""),
                notes=ing.get("original")
            )
            for ing in recipe_data.get("extendedIngredients", [])
        ]
        
        nutrition = None
        if recipe_data.get("nutrition"):
            nutrition = self._extract_nutrition_info(recipe_data["nutrition"])
        
        instructions = []
        if recipe_data.get("instructions"):
            for instruction in recipe_data["instructions"]:
                if isinstance(instruction, dict) and instruction.get("steps"):
                    for step in instruction["steps"]:
                        instructions.append(step.get("step", ""))
                elif isinstance(instruction, str):
                    instructions.append(instruction)
        
        return Recipe(
            id=str(recipe_data.get("id")),
            title=recipe_data.get("title", ""),
            description=recipe_data.get("summary", ""),
            cuisine_type=recipe_data.get("cuisines", [None])[0],
            dietary_tags=recipe_data.get("diets", []),
            prep_time_minutes=recipe_data.get("preparationMinutes", 0),
            cook_time_minutes=recipe_data.get("cookingMinutes", 0),
            total_time_minutes=recipe_data.get("readyInMinutes", 0),
            servings=recipe_data.get("servings", 1),
            ingredients=ingredients,
            instructions=instructions,
            nutrition=nutrition,
            equipment_required=recipe_data.get("equipment", []),
            image_url=recipe_data.get("image"),
            source_url=recipe_data.get("sourceUrl"),
            source="spoonacular"
        )
    
    def _extract_ingredients(self, raw_ingredients: List[Dict]) -> List[Dict]:
        """Extract and format ingredient information."""
        ingredients = []
        
        for ingredient in raw_ingredients:
            ingredients.append({
                "name": ingredient.get("name"),
                "amount": ingredient.get("amount"),
                "unit": ingredient.get("unit"),
                "original_text": ingredient.get("original")
            })
        
        return ingredients
    
    def _extract_nutrition(self, raw_nutrition: Dict) -> Dict:
        """Extract nutrition information."""
        if not raw_nutrition or "nutrients" not in raw_nutrition:
            return {}
        
        nutrition = {}
        for nutrient in raw_nutrition["nutrients"]:
            name = nutrient.get("name", "").lower()
            if name in ["calories", "protein", "carbohydrates", "fat"]:
                nutrition[name] = nutrient.get("amount", 0)
        
        return nutrition
    
    def _extract_nutrition_info(self, raw_nutrition: Dict) -> Optional[NutritionInfo]:
        """Extract nutrition information into NutritionInfo object."""
        if not raw_nutrition or "nutrients" not in raw_nutrition:
            return None
        
        nutrition_data = {}
        for nutrient in raw_nutrition["nutrients"]:
            name = nutrient.get("name", "").lower()
            amount = nutrient.get("amount", 0)
            
            if "calorie" in name:
                nutrition_data["calories_per_serving"] = amount
            elif "protein" in name:
                nutrition_data["protein_grams"] = amount
            elif "carbohydrate" in name:
                nutrition_data["carbs_grams"] = amount
            elif "fat" in name and "saturated" not in name:
                nutrition_data["fat_grams"] = amount
            elif "fiber" in name:
                nutrition_data["fiber_grams"] = amount
            elif "sugar" in name:
                nutrition_data["sugar_grams"] = amount
        
        return NutritionInfo(**nutrition_data) if nutrition_data else None
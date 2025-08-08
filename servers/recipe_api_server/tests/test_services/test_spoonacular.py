import pytest
import sys
import os
from unittest.mock import AsyncMock, patch
from aiohttp import ClientSession

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../..'))

from servers.recipe_api_server.src.services.spoonacular import SpoonacularService

class TestSpoonacularService:
    """Test cases for Spoonacular API service."""
    
    def test_init_without_api_key(self):
        """Test service initialization without API key."""
        with patch.dict(os.environ, {}, clear=True):
            service = SpoonacularService()
            assert service.api_key is None
    
    def test_init_with_api_key(self):
        """Test service initialization with API key."""
        with patch.dict(os.environ, {'SPOONACULAR_API_KEY': 'test_key'}):
            service = SpoonacularService()
            assert service.api_key == 'test_key'
    
    @pytest.mark.asyncio
    async def test_search_recipes_no_api_key(self):
        """Test that search_recipes raises error when no API key is set."""
        with patch.dict(os.environ, {}, clear=True):
            service = SpoonacularService()
            
            with pytest.raises(ValueError, match="SPOONACULAR_API_KEY"):
                await service.search_recipes("test query")
    
    @pytest.mark.asyncio
    async def test_search_recipes_success(self):
        """Test successful recipe search."""
        mock_response_data = {
            "results": [
                {
                    "id": 123,
                    "title": "Test Recipe",
                    "summary": "Test description",
                    "image": "test_image.jpg",
                    "preparationMinutes": 15,
                    "cookingMinutes": 30,
                    "readyInMinutes": 45,
                    "servings": 4,
                    "sourceUrl": "http://test.com",
                    "cuisines": ["Italian"],
                    "diets": ["vegetarian"],
                    "extendedIngredients": [
                        {
                            "name": "tomatoes",
                            "amount": 2,
                            "unit": "cups",
                            "original": "2 cups diced tomatoes"
                        }
                    ],
                    "nutrition": {
                        "nutrients": [
                            {"name": "Calories", "amount": 250},
                            {"name": "Protein", "amount": 15}
                        ]
                    }
                }
            ],
            "totalResults": 1
        }
        
        with patch.dict(os.environ, {'SPOONACULAR_API_KEY': 'test_key'}):
            service = SpoonacularService()
            
            # Mock aiohttp session
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None
            
            mock_session = AsyncMock()
            mock_session.get.return_value.__aenter__.return_value = mock_response
            
            service.session = mock_session
            
            result = await service.search_recipes("test query")
            
            assert result["total_results"] == 1
            assert result["source"] == "spoonacular"
            assert len(result["recipes"]) == 1
            
            recipe = result["recipes"][0]
            assert recipe["id"] == "123"
            assert recipe["title"] == "Test Recipe"
            assert recipe["prep_time_minutes"] == 15
            assert recipe["cook_time_minutes"] == 30
    
    @pytest.mark.asyncio
    async def test_get_recipe_details_not_found(self):
        """Test get_recipe_details when recipe is not found."""
        with patch.dict(os.environ, {'SPOONACULAR_API_KEY': 'test_key'}):
            service = SpoonacularService()
            
            # Mock 404 response
            mock_response = AsyncMock()
            mock_response.raise_for_status.side_effect = Exception("Not found")
            
            mock_session = AsyncMock()
            mock_session.get.return_value.__aenter__.return_value = mock_response
            
            service.session = mock_session
            
            result = await service.get_recipe_details("nonexistent_id")
            
            assert result is None
    
    def test_extract_ingredients(self):
        """Test ingredient extraction from raw API data."""
        service = SpoonacularService()
        
        raw_ingredients = [
            {
                "name": "tomatoes",
                "amount": 2,
                "unit": "cups",
                "original": "2 cups diced tomatoes"
            },
            {
                "name": "onion",
                "amount": 1,
                "unit": "medium",
                "original": "1 medium onion, diced"
            }
        ]
        
        result = service._extract_ingredients(raw_ingredients)
        
        assert len(result) == 2
        assert result[0]["name"] == "tomatoes"
        assert result[0]["amount"] == 2
        assert result[0]["unit"] == "cups"
        assert result[1]["name"] == "onion"
    
    def test_extract_nutrition(self):
        """Test nutrition extraction from raw API data."""
        service = SpoonacularService()
        
        raw_nutrition = {
            "nutrients": [
                {"name": "Calories", "amount": 250},
                {"name": "Protein", "amount": 15},
                {"name": "Carbohydrates", "amount": 30},
                {"name": "Fat", "amount": 10},
                {"name": "Sodium", "amount": 500}  # Should be ignored
            ]
        }
        
        result = service._extract_nutrition(raw_nutrition)
        
        assert result["calories"] == 250
        assert result["protein"] == 15
        assert result["carbohydrates"] == 30
        assert result["fat"] == 10
        assert "sodium" not in result
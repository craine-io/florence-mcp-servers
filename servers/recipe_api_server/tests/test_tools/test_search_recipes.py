import pytest
import asyncio
import sys
import os
from unittest.mock import AsyncMock, patch, MagicMock

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../..'))

from servers.recipe_api_server.src.tools.search_recipes import search_recipes

class TestSearchRecipes:
    """Test cases for recipe search functionality."""
    
    @pytest.mark.asyncio
    async def test_search_recipes_basic_query(self):
        """Test basic recipe search with just a query."""
        mock_spoonacular_response = {
            "recipes": [
                {
                    "id": "1",
                    "title": "Chicken Parmesan",
                    "description": "Delicious chicken dish",
                    "prep_time_minutes": 30,
                    "cook_time_minutes": 45,
                    "servings": 4
                }
            ],
            "total_results": 1,
            "source": "spoonacular"
        }
        
        with patch('servers.recipe_api_server.src.tools.search_recipes.SpoonacularService') as mock_service:
            # Setup mock
            mock_instance = AsyncMock()
            mock_instance.search_recipes.return_value = mock_spoonacular_response
            mock_service.return_value.__aenter__.return_value = mock_instance
            
            # Execute search
            result = await search_recipes(query="chicken")
            
            # Verify results
            assert "recipes" in result
            assert len(result["recipes"]) == 1
            assert result["query"] == "chicken"
            assert result["total_found"] == 1
            assert result["source"] == "spoonacular"
            
            # Verify service was called correctly
            mock_instance.search_recipes.assert_called_once_with(
                query="chicken",
                dietary_restrictions=None,
                cuisine_type=None,
                max_time=None,
                number=10
            )
    
    @pytest.mark.asyncio
    async def test_search_recipes_with_filters(self):
        """Test recipe search with dietary restrictions and cuisine filters."""
        mock_response = {
            "recipes": [],
            "total_results": 0,
            "source": "spoonacular"
        }
        
        with patch('servers.recipe_api_server.src.tools.search_recipes.SpoonacularService') as mock_service:
            mock_instance = AsyncMock()
            mock_instance.search_recipes.return_value = mock_response
            mock_service.return_value.__aenter__.return_value = mock_instance
            
            # Execute search with filters
            result = await search_recipes(
                query="pasta",
                dietary_restrictions=["vegetarian"],
                cuisine_type="italian",
                max_time=60,
                number=5
            )
            
            # Verify filters were passed to service
            mock_instance.search_recipes.assert_called_once_with(
                query="pasta",
                dietary_restrictions=["vegetarian"],
                cuisine_type="italian",
                max_time=60,
                number=5
            )
            
            # Verify filters are in response
            assert result["filters_applied"]["dietary_restrictions"] == ["vegetarian"]
            assert result["filters_applied"]["cuisine_type"] == "italian"
            assert result["filters_applied"]["max_time"] == 60
    
    @pytest.mark.asyncio
    async def test_search_recipes_handles_api_failure(self):
        """Test that search handles API failures gracefully."""
        with patch('servers.recipe_api_server.src.tools.search_recipes.SpoonacularService') as mock_service:
            # Setup failing service
            mock_instance = AsyncMock()
            mock_instance.search_recipes.side_effect = Exception("API Error")
            mock_service.return_value.__aenter__.return_value = mock_instance
            
            # Execute search
            result = await search_recipes(query="test")
            
            # Should return error response but not crash
            assert result["recipes"] == []
            assert result["total_found"] == 0
            assert "error" in result
            assert result["error"] == "API Error"
    
    def test_sort_by_relevance(self):
        """Test recipe relevance sorting."""
        from servers.recipe_api_server.src.tools.search_recipes import _sort_by_relevance
        
        recipes = [
            {"title": "Beef Stroganoff", "description": "Creamy beef dish"},
            {"title": "Chicken Parmesan", "description": "Italian chicken with parmesan"},
            {"title": "Parmesan Chicken Salad", "description": "Fresh salad with chicken"}
        ]
        
        sorted_recipes = _sort_by_relevance(recipes, "chicken parmesan")
        
        # Recipes with more matches should be first
        assert "Chicken Parmesan" in sorted_recipes[0]["title"]
        assert "Parmesan Chicken Salad" in sorted_recipes[1]["title"]
        assert "Beef Stroganoff" in sorted_recipes[2]["title"]
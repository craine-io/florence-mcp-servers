import pytest
import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from shared.types import Recipe, Ingredient, NutritionInfo

class TestIngredient:
    """Test cases for Ingredient model."""
    
    def test_ingredient_creation(self):
        """Test basic ingredient creation."""
        ingredient = Ingredient(
            name="tomatoes",
            amount=2.0,
            unit="cups",
            notes="diced"
        )
        
        assert ingredient.name == "tomatoes"
        assert ingredient.amount == 2.0
        assert ingredient.unit == "cups"
        assert ingredient.notes == "diced"
    
    def test_ingredient_to_dict(self):
        """Test ingredient serialization to dictionary."""
        ingredient = Ingredient(
            name="onion",
            amount=1.0,
            unit="medium"
        )
        
        result = ingredient.to_dict()
        
        expected = {
            "name": "onion",
            "amount": 1.0,
            "unit": "medium",
            "notes": None
        }
        
        assert result == expected
    
    def test_ingredient_from_dict(self):
        """Test ingredient deserialization from dictionary."""
        data = {
            "name": "garlic",
            "amount": 3.0,
            "unit": "cloves",
            "notes": "minced"
        }
        
        ingredient = Ingredient.from_dict(data)
        
        assert ingredient.name == "garlic"
        assert ingredient.amount == 3.0
        assert ingredient.unit == "cloves"
        assert ingredient.notes == "minced"

class TestNutritionInfo:
    """Test cases for NutritionInfo model."""
    
    def test_nutrition_creation(self):
        """Test nutrition info creation."""
        nutrition = NutritionInfo(
            calories_per_serving=250.0,
            protein_grams=15.0,
            carbs_grams=30.0,
            fat_grams=10.0
        )
        
        assert nutrition.calories_per_serving == 250.0
        assert nutrition.protein_grams == 15.0
        assert nutrition.carbs_grams == 30.0
        assert nutrition.fat_grams == 10.0
    
    def test_nutrition_to_dict(self):
        """Test nutrition info serialization."""
        nutrition = NutritionInfo(calories_per_serving=200.0)
        
        result = nutrition.to_dict()
        
        assert result["calories_per_serving"] == 200.0
        assert result["protein_grams"] is None

class TestRecipe:
    """Test cases for Recipe model."""
    
    def test_recipe_creation(self):
        """Test basic recipe creation."""
        ingredients = [
            Ingredient("tomatoes", 2.0, "cups"),
            Ingredient("onion", 1.0, "medium")
        ]
        
        nutrition = NutritionInfo(calories_per_serving=300.0)
        
        recipe = Recipe(
            id="test123",
            title="Test Recipe",
            description="A test recipe",
            ingredients=ingredients,
            nutrition=nutrition,
            servings=4
        )
        
        assert recipe.id == "test123"
        assert recipe.title == "Test Recipe"
        assert len(recipe.ingredients) == 2
        assert recipe.nutrition.calories_per_serving == 300.0
        assert recipe.servings == 4
    
    def test_recipe_to_dict(self):
        """Test recipe serialization to dictionary."""
        ingredient = Ingredient("salt", 1.0, "tsp")
        recipe = Recipe(
            id="test456",
            title="Simple Recipe",
            ingredients=[ingredient],
            servings=2
        )
        
        result = recipe.to_dict()
        
        assert result["id"] == "test456"
        assert result["title"] == "Simple Recipe"
        assert result["servings"] == 2
        assert len(result["ingredients"]) == 1
        assert result["ingredients"][0]["name"] == "salt"
    
    def test_recipe_from_dict(self):
        """Test recipe deserialization from dictionary."""
        data = {
            "id": "test789",
            "title": "Dict Recipe",
            "description": "From dictionary",
            "servings": 3,
            "ingredients": [
                {"name": "pepper", "amount": 0.5, "unit": "tsp", "notes": None}
            ],
            "nutrition": {
                "calories_per_serving": 150.0,
                "protein_grams": 5.0
            },
            "created_at": "2024-01-01T12:00:00",
            "updated_at": "2024-01-01T12:00:00"
        }
        
        recipe = Recipe.from_dict(data)
        
        assert recipe.id == "test789"
        assert recipe.title == "Dict Recipe"
        assert recipe.servings == 3
        assert len(recipe.ingredients) == 1
        assert recipe.ingredients[0].name == "pepper"
        assert recipe.nutrition.calories_per_serving == 150.0
    
    def test_recipe_scale(self):
        """Test recipe scaling functionality."""
        ingredients = [
            Ingredient("flour", 2.0, "cups"),
            Ingredient("sugar", 1.0, "cup")
        ]
        
        original_recipe = Recipe(
            id="scale_test",
            title="Original Recipe",
            ingredients=ingredients,
            servings=4
        )
        
        scaled_recipe = original_recipe.scale_recipe(8)  # Double the recipe
        
        assert scaled_recipe.servings == 8
        assert scaled_recipe.ingredients[0].amount == 4.0  # 2 * 2
        assert scaled_recipe.ingredients[1].amount == 2.0  # 1 * 2
        assert "serves 8" in scaled_recipe.title
    
    def test_recipe_scale_zero_servings(self):
        """Test that scaling fails with zero or negative servings."""
        recipe = Recipe(
            id="bad_scale",
            title="Bad Recipe",
            servings=0
        )
        
        with pytest.raises(ValueError, match="Cannot scale recipe"):
            recipe.scale_recipe(4)
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import json

@dataclass
class Ingredient:
    """Represents a recipe ingredient."""
    name: str
    amount: float
    unit: str
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "amount": self.amount,
            "unit": self.unit,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Ingredient":
        return cls(
            name=data["name"],
            amount=data["amount"],
            unit=data["unit"],
            notes=data.get("notes")
        )

@dataclass
class NutritionInfo:
    """Represents nutrition information."""
    calories_per_serving: Optional[float] = None
    protein_grams: Optional[float] = None
    carbs_grams: Optional[float] = None
    fat_grams: Optional[float] = None
    fiber_grams: Optional[float] = None
    sugar_grams: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "calories_per_serving": self.calories_per_serving,
            "protein_grams": self.protein_grams,
            "carbs_grams": self.carbs_grams,
            "fat_grams": self.fat_grams,
            "fiber_grams": self.fiber_grams,
            "sugar_grams": self.sugar_grams
        }

@dataclass
class Recipe:
    """Represents a recipe with all its components."""
    id: str
    title: str
    description: str = ""
    cuisine_type: Optional[str] = None
    dietary_tags: List[str] = field(default_factory=list)
    prep_time_minutes: int = 0
    cook_time_minutes: int = 0
    total_time_minutes: int = 0
    servings: int = 1
    difficulty_level: str = "intermediate"
    ingredients: List[Ingredient] = field(default_factory=list)
    instructions: List[str] = field(default_factory=list)
    nutrition: Optional[NutritionInfo] = None
    equipment_required: List[str] = field(default_factory=list)
    image_url: Optional[str] = None
    source_url: Optional[str] = None
    source: str = "unknown"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert recipe to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "cuisine_type": self.cuisine_type,
            "dietary_tags": self.dietary_tags,
            "prep_time_minutes": self.prep_time_minutes,
            "cook_time_minutes": self.cook_time_minutes,
            "total_time_minutes": self.total_time_minutes,
            "servings": self.servings,
            "difficulty_level": self.difficulty_level,
            "ingredients": [ing.to_dict() for ing in self.ingredients],
            "instructions": self.instructions,
            "nutrition": self.nutrition.to_dict() if self.nutrition else None,
            "equipment_required": self.equipment_required,
            "image_url": self.image_url,
            "source_url": self.source_url,
            "source": self.source,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Recipe":
        """Create recipe from dictionary."""
        ingredients = [
            Ingredient.from_dict(ing_data) 
            for ing_data in data.get("ingredients", [])
        ]
        
        nutrition = None
        if data.get("nutrition"):
            nutrition = NutritionInfo(**data["nutrition"])
        
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            cuisine_type=data.get("cuisine_type"),
            dietary_tags=data.get("dietary_tags", []),
            prep_time_minutes=data.get("prep_time_minutes", 0),
            cook_time_minutes=data.get("cook_time_minutes", 0),
            total_time_minutes=data.get("total_time_minutes", 0),
            servings=data.get("servings", 1),
            difficulty_level=data.get("difficulty_level", "intermediate"),
            ingredients=ingredients,
            instructions=data.get("instructions", []),
            nutrition=nutrition,
            equipment_required=data.get("equipment_required", []),
            image_url=data.get("image_url"),
            source_url=data.get("source_url"),
            source=data.get("source", "unknown"),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat()))
        )
    
    def scale_recipe(self, new_servings: int) -> "Recipe":
        """Scale recipe to new serving size."""
        if self.servings <= 0:
            raise ValueError("Cannot scale recipe with zero or negative servings")
        
        scale_factor = new_servings / self.servings
        
        scaled_ingredients = []
        for ingredient in self.ingredients:
            scaled_ingredients.append(Ingredient(
                name=ingredient.name,
                amount=ingredient.amount * scale_factor,
                unit=ingredient.unit,
                notes=ingredient.notes
            ))
        
        return Recipe(
            id=f"{self.id}_scaled_{new_servings}",
            title=f"{self.title} (serves {new_servings})",
            description=self.description,
            cuisine_type=self.cuisine_type,
            dietary_tags=self.dietary_tags.copy(),
            prep_time_minutes=self.prep_time_minutes,
            cook_time_minutes=self.cook_time_minutes,
            total_time_minutes=self.total_time_minutes,
            servings=new_servings,
            difficulty_level=self.difficulty_level,
            ingredients=scaled_ingredients,
            instructions=self.instructions.copy(),
            nutrition=self.nutrition,
            equipment_required=self.equipment_required.copy(),
            image_url=self.image_url,
            source_url=self.source_url,
            source=self.source
        )
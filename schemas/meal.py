from pydantic import BaseModel
from datetime import date
from typing import Optional, List


class MealPath(BaseModel):
    meal_id: int

class MealItemSchema(BaseModel):
    food_id: int
    quantity: float = 1.0

class MealSchema(BaseModel):
    day: Optional[date] = None
    meal_type: str = "breakfast"
    items: List[MealItemSchema] = []

class MealQuery(BaseModel):
    date: Optional[str] = None
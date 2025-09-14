from pydantic import BaseModel

class FoodSchema(BaseModel):
    name: str
    calories: float
    amount: float = 100
    unit: str = "g"
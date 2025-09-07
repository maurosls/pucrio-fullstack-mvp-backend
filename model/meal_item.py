from typing import Any, Dict
from model.db import db

class MealItem(db.Model):
    __tablename__ = "meal_item"

    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey("meal.id"), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey("food.id"), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1.0)

    meal = db.relationship("Meal", back_populates="items")
    food = db.relationship("Food")

    def calories(self) -> float:
        return (self.quantity or 0.0) * (self.food.calories if self.food else 0.0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "food": self.food.to_dict() if self.food else None,
            "quantity": self.quantity,
            "calories": self.calories(),
        }

    def __repr__(self) -> str:
        return f"<MealItem food_id={self.food_id} qty={self.quantity}>"

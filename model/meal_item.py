from typing import Any, Dict, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, ForeignKey
from .base import Base

class MealItem(Base):
    __tablename__ = "meal_item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    meal_id: Mapped[int] = mapped_column(ForeignKey("meal.id"), nullable=False)
    food_id: Mapped[int] = mapped_column(ForeignKey("food.id"), nullable=False)

    quantity: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

    meal: Mapped["Meal"] = relationship("Meal", back_populates="items")
    food: Mapped[Optional["Food"]] = relationship("Food")

    def calories(self) -> float:
        return (self.quantity or 0.0) * (self.food.calories if self.food else 0.0)

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            id=self.id,
            food=self.food.to_dict() if self.food else None,
            quantity=self.quantity,
            calories=self.calories(),
        )

    def __repr__(self) -> str:
        return f"<MealItem food_id={self.food_id} qty={self.quantity}>"

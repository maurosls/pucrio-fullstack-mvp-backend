from typing import Any, Dict
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer
from .base import Base

class Food(Base):
    __tablename__ = "food"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    calories: Mapped[float] = mapped_column(Float, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    unit: Mapped[str] = mapped_column(String(32), nullable=False, default="g")

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            id=self.id,
            name=self.name,
            calories=self.calories,
            amount=self.amount,
            unit=self.unit,
        )

    def __repr__(self) -> str:
        return f"<Food {self.name} {self.calories} kcal per {self.amount}{self.unit}>"

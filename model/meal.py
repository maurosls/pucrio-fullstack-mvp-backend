from typing import Any, Dict
from datetime import datetime
from model.db import db
from model.enums import MealType

class Meal(db.Model):
    __tablename__ = "meal"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    meal_type = db.Column(db.Enum(MealType, name="meal_type", native_enum=False, validate_strings=True),
        nullable=False,
        index=True,
        )

    items = db.relationship(
        "MealItem",
        back_populates="meal",
        cascade="all, delete-orphan",
    )

    def total_calories(self) -> float:
        return sum(item.calories() for item in (self.items or []))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "day": self.day.isoformat(),
            "meal_type": self.meal_type.value,
            "total_calories": self.total_calories(),
            "items": [i.to_dict() for i in (self.items or [])],
        }

    def __repr__(self) -> str:
        return f"<Meal id={self.id} day={self.day} items={len(self.items or [])}>"

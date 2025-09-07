from typing import Any, Dict
from datetime import datetime
from model.db import db

class Meal(db.Model):
    __tablename__ = "meal"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date, nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

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
            "total_calories": self.total_calories(),
            "items": [i.to_dict() for i in (self.items or [])],
        }

    def __repr__(self) -> str:
        return f"<Meal id={self.id} day={self.day} items={len(self.items or [])}>"

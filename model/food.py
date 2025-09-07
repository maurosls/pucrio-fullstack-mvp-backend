from typing import Any, Dict
from model.db import db

from .base import Base

class Food(db.Model):
    __tablename__ = "food"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    calories = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False, default=100.0)
    unit = db.Column(db.String(32), nullable=False, default="g")

    def to_dict(self) -> Dict[str, Any]:
        return dict(id=self.id, name=self.name, calories=self.calories,
                    amount=self.amount, unit=self.unit)

from typing import Any, Dict, List
from datetime import datetime, date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Date as SADate, DateTime
from .base import Base

class Meal(Base):
    __tablename__ = "meal"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    day: Mapped[date] = mapped_column(SADate, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    items: Mapped[List["MealItem"]] = relationship(
        "MealItem", back_populates="meal", cascade="all, delete-orphan"
    )

    def total_calories(self) -> float:
        return sum(item.calories() for item in self.items or [])

    def to_dict(self) -> Dict[str, Any]:
        return dict(
            id=self.id,
            day=self.day.isoformat(),
            total_calories=self.total_calories(),
            items=[i.to_dict() for i in self.items or []],
        )

    def __repr__(self) -> str:
        return f"<Meal id={self.id} day={self.day} items={len(self.items or [])}>"

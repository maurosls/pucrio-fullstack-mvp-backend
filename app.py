from __future__ import annotations
from flask_openapi3 import OpenAPI, Info
from model.db import insert_initial_items, db
from typing import Optional, List

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from model import food
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import inspect
from datetime import date
from pydantic import BaseModel

info = Info(title="Meal Tracker API", version="1.0.0")
app = OpenAPI(__name__, info=info)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    from model.food import Food
    from model.meal import Meal
    from model.meal_item import MealItem
    db.create_all()
    insert_initial_items()

class MealPath(BaseModel):
    meal_id: int

class MealItemIn(BaseModel):
    food_id: int
    quantity: float = 1.0

class MealIn(BaseModel):
    day: Optional[date] = None
    meal_type: str = "breakfast"
    items: List[MealItemIn] = []

def extractFoodData(payload: dict) -> Food:
    name = (payload.get("name") or "").strip()
    calories = payload.get("calories")
    amount = payload.get("amount", 100)
    unit = (payload.get("unit") or "g").strip() or "g"
    return Food(name=name, calories=calories, amount=amount, unit=unit)


@app.get("/foods")
def list_foods():
    print(inspect(db.engine).get_columns("meal"))
    foods = Food.query.all()
    return jsonify([f.to_dict() for f in foods])

@app.post("/foods")
def create_food():
    payload = request.get_json(silent=True) or {}
    f = extractFoodData(payload)
    db.session.add(f)
    db.session.commit()
    return jsonify(f.to_dict()), 201

@app.post("/meals")
def create_meal(body: MealIn):

    day = body.day or date.today()
    meal_type = body.meal_type
    meal = Meal(day=day, meal_type=meal_type)    
    
    db.session.add(meal)

    for it in body.items:
        food = Food.query.get(it.food_id)
        db.session.add(MealItem(meal=meal, food=food, quantity=it.quantity))

    db.session.commit()
    return jsonify(meal.to_dict()), 201

@app.get("/meals")
def list_meals_for_day():
    q = (Meal.query
         .options(
            joinedload(Meal.items)
            .joinedload(MealItem.food))
         .order_by(Meal.day.asc(), Meal.day.asc()))
    
    date_str = request.args.get("date")

    if date_str:
        d = date.fromisoformat(date_str)
        q = q.filter(Meal.day == d)

    meals = q.all()
    return jsonify([m.to_dict() for m in meals]), 200

@app.get("/meals/<int:meal_id>")
def get_meal(path: MealPath):
    meal = (
        Meal.query
        .options(selectinload(Meal.items).joinedload(MealItem.food))
        .filter(Meal.id == path.meal_id)
        .first()
    )
    if not meal:
        return jsonify({"error": "meal not found"}), 404
    return jsonify(meal.to_dict()), 200


@app.post("/meals/<int:meal_id>/items")
def add_item(path: MealPath, body: MealItemIn):
    meal = Meal.query.get(path.meal_id)
    food = Food.query.get(body.food_id)

    item = MealItem(meal=meal, food=food, quantity=body.quantity)
    db.session.add(item)
    db.session.commit()

    meal = (
        Meal.query
        .options(selectinload(Meal.items).joinedload(MealItem.food))
        .get(path.meal_id)
    )
    return jsonify({"item": item.to_dict(), "meal": meal.to_dict()}), 201

@app.get("/total")
def total_for_day():
    from model.meal import Meal

    qs = request.args.get("date")           # str | None
    d = date.fromisoformat(qs) if qs else date.today()

    meals = Meal.query.filter(Meal.day == d).all()
    total = sum(m.total_calories() for m in meals)
    breakdown = [
        {"meal_id": m.id,
         "meal_type": (m.meal_type.value if hasattr(m.meal_type, "value") else m.meal_type),
         "calories": m.total_calories()}
        for m in meals
    ]
    return jsonify({"date": d.isoformat(), "total_calories": total, "meals": breakdown}), 200

if __name__ == "__main__":
    app.run(debug=True)
    print(inspect(db.engine).get_columns("meal"))

from __future__ import annotations
from flask_openapi3 import OpenAPI, Info
from model.db import insert_initial_items, db

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from model import food

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

# Return all existing foods
@app.get("/foods")
def list_foods():
    foods = Food.query.all()
    return jsonify([f.to_dict() for f in foods])

# Insert a new meal
@app.post("/meals")
def create_meal():
    print("/meals")
    #to do

# Return all existing meals
@app.get("/meals")
def list_meals_for_day():
    meals = Meal.query.order_by(Meal.day.asc()).all()
    return jsonify([f.to_dict() for f in meals])

#rReturn specific meal
@app.get("/meals/<int:meal_id>")
def get_meal(meal_id: int):
    print("/meals/<int:meal_id>")
    #to do

# Insert food (items) in a meal
@app.post("/meals/<int:meal_id>/items")
def add_item(meal_id: int):
    print("/meals/<int:meal_id>/items")
    #to do

@app.get("/total")
def total_for_day():
    print("/total")
    #to do


if __name__ == "__main__":
    app.run(debug=True)

from __future__ import annotations
from datetime import date, datetime
from typing import List, Dict, Any, Optional

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from model import meal, food, meal_item

# Return all existing foods
@app.get("/foods")
def list_foods():
    print("/foods")

# Insert a new meal
@app.post("/meals")
def create_meal():
    print("/meals")

# Return all existing meals
@app.get("/meals")
def list_meals_for_day():
    print("/meals")

#rReturn specific meal
@app.get("/meals/<int:meal_id>")
def get_meal(meal_id: int):
    print("/meals/<int:meal_id>")

# Insert food (items) in a meal
@app.post("/meals/<int:meal_id>/items")
def add_item(meal_id: int):
    print("/meals/<int:meal_id>/items")


@app.get("/total")
def total_for_day():
    print("/total")


if __name__ == "__main__":
    app.run(debug=True)

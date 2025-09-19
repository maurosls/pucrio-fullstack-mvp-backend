from __future__ import annotations
from flask_openapi3 import OpenAPI, Info, Tag
from model.db import insert_initial_items, db
from flask_cors import CORS

from flask import jsonify, request
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import inspect
from datetime import date

from schemas.food import FoodSchema
from schemas.meal import MealSchema, MealItemSchema, MealPath, MealQuery

info = Info(title="Meal Tracker API", version="1.0.0")
app = OpenAPI(__name__, info=info)

meal_tag = Tag(name="Refeições", description="Operações relacionadas a refeições")
food_tag = Tag(name="Alimentos", description="Operações relacionadas a alimentos")
others_tag = Tag(name="Outros", description="Outras operações")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
CORS(app)

with app.app_context():
    from model.food import Food
    from model.meal import Meal
    from model.meal_item import MealItem
    db.create_all()
    insert_initial_items()

def extractFoodData(payload: dict) -> Food:
    name = (payload.get("name") or "").strip()
    calories = payload.get("calories")
    amount = payload.get("amount", 100)
    unit = (payload.get("unit") or "g").strip() or "g"
    return Food(name=name, calories=calories, amount=amount, unit=unit)


@app.get("/foods", tags=[food_tag], description="Listar todos os alimentos")
def list_foods():
    print(inspect(db.engine).get_columns("meal"))
    foods = Food.query.all()
    return jsonify([f.to_dict() for f in foods])

@app.post("/foods", tags=[food_tag], description="Criar um novo alimento")
def create_food(body: FoodSchema):
    payload = request.get_json(silent=True) or {}
    f = extractFoodData(payload)
    db.session.add(f)
    db.session.commit()
    return jsonify(f.to_dict()), 201

@app.post("/meals", tags=[meal_tag], description="Criar uma nova refeição")
def create_meal(body: MealSchema):

    day = body.day or date.today()
    meal_type = body.meal_type
    meal = Meal(day=day, meal_type=meal_type)    
    
    db.session.add(meal)

    for it in body.items:
        food = Food.query.get(it.food_id)
        db.session.add(MealItem(meal=meal, food=food, quantity=it.quantity))

    db.session.commit()
    return jsonify(meal.to_dict()), 201

@app.get("/meals", tags=[meal_tag], description="Listar todas as refeições, opcionalmente filtrando por dia")
def list_meals_for_day(query: MealQuery):
    q = (Meal.query
         .options(
            joinedload(Meal.items)
            .joinedload(MealItem.food))
         .order_by(Meal.day.asc(), Meal.day.asc()))
    
    if query.date:
        d = date.fromisoformat(query.date)
        q = q.filter(Meal.day == d)

    meals = q.all()
    return jsonify([m.to_dict() for m in meals]), 200

@app.get("/meals/<int:meal_id>", tags=[meal_tag], description="Obter detalhes de uma refeição específica")
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


@app.post("/meals/<int:meal_id>/items", tags=[meal_tag], description="Adicionar um item a uma refeição existente")
def add_item(path: MealPath, body: MealItemSchema):
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

@app.get("/total", tags=[others_tag], description="Obter o total de calorias consumidas em um dia específico")
def total_for_day():
    from model.meal import Meal

    qs = request.args.get("date")
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

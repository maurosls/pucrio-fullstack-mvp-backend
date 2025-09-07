from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta

db = SQLAlchemy()

DATABASE_URL = "sqlite:///app.db"

def insert_initial_items() -> None:
    from model.food import Food
    from model.meal import Meal
    from model.meal_item import MealItem
    if db.session.query(Food.id).first():
        return

    food_catalog = [
        dict(name="Banana",        calories=89,   amount=100, unit="g"),
        dict(name="Apple",         calories=52,   amount=100, unit="g"),
        dict(name="Rice (cooked)", calories=130,  amount=100, unit="g"),
        dict(name="Chicken breast (grilled)", calories=165, amount=100, unit="g"),
        dict(name="Whole egg",     calories=78,   amount=1,   unit="unit"),
        dict(name="Greek yogurt (plain)", calories=59, amount=100, unit="g"),
        dict(name="Olive oil",     calories=884,  amount=100, unit="ml"),
    ]

    db.session.bulk_insert_mappings(Food, food_catalog)
    db.session.commit()
    foods = {f.name: f for f in db.session.query(Food).all()}

    today = date.today()

    breakfast_today = Meal(day=today)
    breakfast_today.items = [
            MealItem(food=foods["Greek yogurt (plain)"], quantity=2.0),  
            MealItem(food=foods["Banana"], quantity=1.0),               
        ]
    
    db.session.add_all([
            breakfast_today
        ])
    db.session.commit()

    
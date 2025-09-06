from datetime import date
from db import init_db, SessionLocal
from model.food import Food
from model.meal import Meal
from model.meal_item import MealItem
from sqlalchemy.orm import Session

def initialize_db(session: Session) -> None:
    exists = session.query(Food.id).limit(1).first()
    if exists:
        return

    catalog = [
        dict(name="Banana",        calories=89,   amount=100, unit="g"),
        dict(name="Apple",         calories=52,   amount=100, unit="g"),
        dict(name="Rice (cooked)", calories=130,  amount=100, unit="g"),
        dict(name="Chicken breast (grilled)", calories=165, amount=100, unit="g"),
        dict(name="Whole egg",     calories=78,   amount=1,   unit="unit"),
        dict(name="Greek yogurt (plain)", calories=59, amount=100, unit="g"),
        dict(name="Olive oil",     calories=884,  amount=100, unit="ml"),
    ]
    session.bulk_insert_mappings(Food, catalog)
    session.commit()


def main():
    init_db()
    with SessionLocal() as s:
        initialize_db(s)

        banana = s.query(Food).filter_by(name="Banana").one()
        chicken = s.query(Food).filter_by(name="Chicken breast (grilled)").one()

        meal = Meal(day=date.today())
        s.add(meal)
        s.flush()

        s.add_all([
            MealItem(meal_id=meal.id, food_id=banana.id, quantity=1.5),
            MealItem(meal_id=meal.id, food_id=chicken.id, quantity=2.0),
        ])
        s.commit()

        # reload with relationships
        reloaded = s.query(Meal).filter_by(id=meal.id).one()
        print("Meal:", reloaded)
        print("Items:", [i.to_dict() for i in reloaded.items])
        print("Total calories:", reloaded.total_calories())
        print("As dict:", reloaded.to_dict())

if __name__ == "__main__":
    main()

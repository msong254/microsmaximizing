from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from pydantic import BaseModel

from database.db import get_db
from database.models.food import Food
from database.models.nutrient import Nutrient
from database.models.food_nutrient import FoodNutrient
from database.models.log import FoodLog

router = APIRouter()

class LogRequest(BaseModel):
    food_id: int
    amount: float

@router.get("/foods/search")
def search_foods(query: str, db: Session = Depends(get_db)):
    print(f"🔍 Searching for: {query}")
    try:
        results = (
            db.query(Food)
            .filter(Food.name.ilike(f"%{query}%"))
            .order_by(
                (Food.name.ilike(query)).desc(),
                (Food.name.ilike(f"{query}%")).desc(),
                Food.name
            )
            .limit(20)
            .all()
        )
        return [{"id": food.id, "name": food.name} for food in results]
    except Exception as e:
        print(f"❌ Error during food search: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/log")
def log_food(entry: LogRequest, db: Session = Depends(get_db)):
    food = db.query(Food).filter(Food.id == entry.food_id).first()
    if not food:
        raise HTTPException(status_code=400, detail="Invalid food ID — please select a valid food.")
    
    log = FoodLog(food_id=entry.food_id, amount=entry.amount, log_date=date.today())
    db.add(log)
    db.commit()
    return {"message": "Food logged successfully"}

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    today = date.today()

    logs = db.query(FoodLog).filter(FoodLog.log_date == today).all()
    if not logs:
        return []

    all_nutrients = db.query(Nutrient).all()
    nutrient_lookup = {
        n.id: {
            "name": n.name,
            "unit": n.unit,
            "rda": n.rda.value if hasattr(n.rda, 'value') else n.rda
        } for n in all_nutrients
    }

    food_ids = [log.food_id for log in logs]
    food_nutrients = db.query(FoodNutrient).filter(FoodNutrient.food_id.in_(food_ids)).all()

    food_nutrient_map = {}
    for fn in food_nutrients:
        food_nutrient_map.setdefault(fn.food_id, []).append(fn)

    nutrient_totals = {}
    for log in logs:
        fns = food_nutrient_map.get(log.food_id, [])
        for fn in fns:
            added_amt = (fn.amount / 100.0) * log.amount
            if fn.nutrient_id not in nutrient_totals:
                nutrient_totals[fn.nutrient_id] = 0.0
            nutrient_totals[fn.nutrient_id] += added_amt

    result = []
    for nid, total in nutrient_totals.items():
        info = nutrient_lookup.get(nid)
        if info:
            result.append({
                "id": nid,
                "name": info["name"],
                "unit": info["unit"],
                "total": round(total, 2),
                "rda": info["rda"]
            })

    return result

@router.get("/micronutrient-from-food")
def get_micronutrients(food_id: int, db: Session = Depends(get_db)):
    food_nutrients = db.query(FoodNutrient).filter(FoodNutrient.food_id == food_id).all()
    
    nutrients = []
    for fn in food_nutrients:
        nutrient = db.query(Nutrient).filter(Nutrient.id == fn.nutrient_id).first()
        if nutrient:
            nutrients.append({
                "nutrient_id": nutrient.id,
                "nutrient_name": nutrient.name,
                "amount": fn.amount,
                "unit": nutrient.unit
            })

    return nutrients

@router.get("/log-history")
def get_log_history(db: Session = Depends(get_db)):
    today = date.today()
    logs = db.query(FoodLog).filter(FoodLog.log_date == today).all()

    food_ids = [log.food_id for log in logs]
    foods = db.query(Food).filter(Food.id.in_(food_ids)).all()
    food_lookup = {food.id: food.name for food in foods}

    result = []
    for log in logs:
        result.append({
            "name": food_lookup.get(log.food_id, "Unknown"),
            "amount": log.amount
        })

    return result

@router.delete("/clear-log")
def clear_log(db: Session = Depends(get_db)):
    db.query(FoodLog).delete()
    db.commit()
    return {"message": "All logs cleared"}
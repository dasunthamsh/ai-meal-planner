from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from meal_recommender import MealRecommender
import joblib

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the recommender
recommender = MealRecommender()
recommender.load_saved_model()  # Assumes you've already trained and saved the model

class UserPreferences(BaseModel):
    calories: int
    dietaryPreference: str = 'none'
    age: int = 30
    gender: str = 'male'
    height: int = 170
    weight: int = 70
    weightGoal: str = 'maintain'

@app.post("/generate-meal-plan")
async def generate_meal_plan(prefs: UserPreferences):
    meal_plan = recommender.generate_meal_plan(
        daily_calories=prefs.calories,
        dietary_preference=prefs.dietaryPreference,
        age=prefs.age,
        gender=prefs.gender,
        height=prefs.height,
        weight=prefs.weight,
        weight_goal=prefs.weightGoal
    )

    # Format the response to match your frontend expectations
    formatted_plan = {
        "breakfast": {
            "name": meal_plan['breakfast']['name'],
            "description": f"A delicious {prefs.dietaryPreference if prefs.dietaryPreference != 'none' else ''} breakfast",
            "ingredients": ["Ingredient 1", "Ingredient 2"],  # Would come from your dataset
            "instructions": ["Step 1", "Step 2"],  # Would come from your dataset
            "calories": meal_plan['breakfast']['calories'],
            "cookTime": meal_plan['breakfast']['prep_time'],
            "protein": meal_plan['breakfast']['protein'],
            "carbs": meal_plan['breakfast']['carbs'],
            "fat": meal_plan['breakfast']['fat']
        },
        "lunch": {
            "name": meal_plan['lunch']['name'],
            "description": f"A balanced {prefs.dietaryPreference if prefs.dietaryPreference != 'none' else ''} lunch",
            "ingredients": ["Ingredient 1", "Ingredient 2"],
            "instructions": ["Step 1", "Step 2"],
            "calories": meal_plan['lunch']['calories'],
            "cookTime": meal_plan['lunch']['prep_time'],
            "protein": meal_plan['lunch']['protein'],
            "carbs": meal_plan['lunch']['carbs'],
            "fat": meal_plan['lunch']['fat']
        },
        "dinner": {
            "name": meal_plan['dinner']['name'],
            "description": f"A satisfying {prefs.dietaryPreference if prefs.dietaryPreference != 'none' else ''} dinner",
            "ingredients": ["Ingredient 1", "Ingredient 2"],
            "instructions": ["Step 1", "Step 2"],
            "calories": meal_plan['dinner']['calories'],
            "cookTime": meal_plan['dinner']['prep_time'],
            "protein": meal_plan['dinner']['protein'],
            "carbs": meal_plan['dinner']['carbs'],
            "fat": meal_plan['dinner']['fat']
        },
        "snacks": [{
            "name": snack['name'],
            "description": f"A quick {prefs.dietaryPreference if prefs.dietaryPreference != 'none' else ''} snack",
            "ingredients": ["Ingredient 1", "Ingredient 2"],
            "instructions": ["Step 1", "Step 2"],
            "calories": snack['calories'],
            "cookTime": snack['prep_time'],
            "protein": snack['protein'],
            "carbs": snack['carbs'],
            "fat": snack['fat']
        } for snack in meal_plan['snacks']],
        "totalCalories": meal_plan['totalCalories'],
        "nutritionalSummary": meal_plan['nutritionalSummary']
    }

    return formatted_plan

@app.get("/")
async def root():
    return {"message": "AI Meal Planner API"}

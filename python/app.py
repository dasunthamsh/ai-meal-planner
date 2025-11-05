from flask import Flask, request, jsonify
from models.genetic_algorithm import MealPlanGeneticAlgorithm
from models.data_preprocessor import DataPreprocessor
import pickle
from config import SCALER_SAVE_PATH, DIET_TYPE_MAPPING, DEFAULT_NUTRITION_TARGETS
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Initialize data preprocessor and load data
preprocessor = DataPreprocessor()
df = preprocessor.load_data()
df, _, _, _ = preprocessor.preprocess_data()

# Initialize Genetic Algorithm
ga = MealPlanGeneticAlgorithm(df)

# Load scaler
with open(SCALER_SAVE_PATH, 'rb') as f:
    scaler = pickle.load(f)

def calculate_target_nutrition(user_data):
    calories = user_data['adjustedCalories']

    # Macronutrient distribution based on goals
    if user_data['goal'] == 'Lose Weight':
        protein_ratio = 0.35
        fat_ratio = 0.25
        carb_ratio = 0.40
    elif user_data['goal'] == 'Build Muscle':
        protein_ratio = 0.40
        fat_ratio = 0.20
        carb_ratio = 0.40
    elif user_data['goal'] == 'Gain Weight':
        protein_ratio = 0.25
        fat_ratio = 0.25
        carb_ratio = 0.50
    else:  # Maintain Weight
        protein_ratio = 0.30
        fat_ratio = 0.30
        carb_ratio = 0.40

    # Calculate grams (4 cal/g for protein and carbs, 9 cal/g for fat)
    protein_g = (calories * protein_ratio) / 4
    fat_g = (calories * fat_ratio) / 9
    carbs_g = (calories * carb_ratio) / 4

    return {
        'calories': calories,
        'protein': protein_g,
        'fat': fat_g,
        'carbs': carbs_g
    }

def apply_health_restrictions(meal, health_risks):
    """Apply restrictions based on health risks"""
    restrictions = {
        'High blood pressure': lambda m: m['sodium_mg'] < 500,
        'High cholesterol': lambda m: m['cholesterol_mg'] < 100 and m['saturated_fat_g'] < 5,
        'Diabetes': lambda m: m['sugar_g'] < 10 and m['added_sugar_g'] < 5,
        'Heart disease or stroke': lambda m: m['saturated_fat_g'] < 5 and m['cholesterol_mg'] < 100 and m['sodium_mg'] < 500,
        'Testosterone deficiency': lambda m: m['omega3_g'] > 0.5,
        'Depression': lambda m: m['omega3_g'] > 0.5
    }

    for risk in health_risks:
        if risk in restrictions and not restrictions[risk](meal):
            return False

    return True

@app.route('/generate-meal-plan', methods=['POST'])
def generate_meal_plan():
    try:
        user_data = request.json

        # Prepare dietary restrictions
        dietary_restrictions = {
            'vegetarian': user_data.get('dietType') == 'Vegetarian',
            'vegan': user_data.get('dietType') == 'Vegan',
            'keto': user_data.get('dietType') == 'Keto',
            'paleo': user_data.get('dietType') == 'Paleo',
            'gluten_free': user_data.get('dietType') == 'Gluten Free',
            'mediterranean': user_data.get('dietType') == 'Mediterranean',
            'allergies': [a.lower() for a in user_data.get('allergies', [])],
            'health_risks': user_data.get('healthRisks', [])
        }

        # Calculate targets
        target_nutrition = calculate_target_nutrition(user_data)
        days = user_data.get('days', 7)

        # Generate meal plan using Genetic Algorithm
        best_solution = ga.evolve(target_nutrition, dietary_restrictions, days)

        # Convert GA solution to meal plan format
        meal_plan = []
        current_nutrition = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}

        for day_idx, day_meals in enumerate(best_solution):
            daily_meals = {'day': day_idx + 1, 'meals': [], 'totalNutrition': {}}

            for meal_type, meal_idx in day_meals.items():
                selected_meal = df.iloc[meal_idx]

                # Check health restrictions
                meal_dict = selected_meal.to_dict()
                if not apply_health_restrictions(meal_dict, dietary_restrictions['health_risks']):
                    # Skip this meal if it violates health restrictions
                    continue

                # Update nutrition (values are per 100g)
                serving_size = 100
                current_nutrition['calories'] += selected_meal['calories'] * scaler.data_max_[0] * (serving_size / 100)
                current_nutrition['protein'] += selected_meal['protein'] * scaler.data_max_[1] * (serving_size / 100)
                current_nutrition['fat'] += selected_meal['fat'] * scaler.data_max_[2] * (serving_size / 100)
                current_nutrition['carbs'] += selected_meal['carbs'] * scaler.data_max_[3] * (serving_size / 100)

                # Add meal to plan
                meal_data = {
                    'meal_name': selected_meal['meal_name'],
                    'calories': float(selected_meal['calories'] * scaler.data_max_[0] * (serving_size / 100)),
                    'protein': float(selected_meal['protein'] * scaler.data_max_[1] * (serving_size / 100)),
                    'fat': float(selected_meal['fat'] * scaler.data_max_[2] * (serving_size / 100)),
                    'carbs': float(selected_meal['carbs'] * scaler.data_max_[3] * (serving_size / 100)),
                    'image_url': selected_meal['image_url'],
                    'vitamins': selected_meal['vitamins'],
                    'ingredients': selected_meal['ingredients'].split(', ') if isinstance(selected_meal['ingredients'], str) else [],
                    'sodium': float(selected_meal['sodium_mg']),
                    'sugar': float(selected_meal['sugar_g']),
                    'fiber': float(selected_meal['fiber_g']),
                    'cholesterol': float(selected_meal['cholesterol_mg'])
                }
                daily_meals['meals'].append({meal_type: meal_data})

            # Add daily totals
            daily_meals['totalNutrition'] = {
                'calories': float(current_nutrition['calories']),
                'protein': float(current_nutrition['protein']),
                'fat': float(current_nutrition['fat']),
                'carbs': float(current_nutrition['carbs'])
            }

            meal_plan.append(daily_meals)
            # Reset for next day (carry over some nutrition)
            current_nutrition = {k: v * 0.3 for k, v in current_nutrition.items()}

        # Calculate overall nutrition summary
        total_calories = sum(day['totalNutrition']['calories'] for day in meal_plan)
        avg_calories = total_calories / days

        response = {
            'mealPlan': meal_plan,
            'nutritionSummary': {
                'avgCalories': avg_calories,
                'avgProtein': sum(day['totalNutrition']['protein'] for day in meal_plan) / days,
                'avgFat': sum(day['totalNutrition']['fat'] for day in meal_plan) / days,
                'avgCarbs': sum(day['totalNutrition']['carbs'] for day in meal_plan) / days,
                'totalDays': days
            }
        }
        return jsonify(response)

    except Exception as e:
        print(f"Error generating meal plan: {e}")
        return jsonify({'error': 'Failed to generate meal plan'}), 500

if __name__ == '__main__':
    app.run(debug=True)

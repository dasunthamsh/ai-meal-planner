# app.py

from flask import Flask, request, jsonify
from models.genetic_algorithm import MealPlanGeneticAlgorithm
from models.data_preprocessor import DataPreprocessor
import pickle
from config import (
    SCALER_SAVE_PATH,
    DEFAULT_DAYS,
    NUTRITION_COLS,
    PORTION_MULTIPLIERS,
    MEAL_TYPES
)
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Load data and initialize once at startup
preprocessor = DataPreprocessor()
df = preprocessor.load_data()
df, _, _, _ = preprocessor.preprocess_data()

# Load scaler with columns
with open(SCALER_SAVE_PATH, 'rb') as f:
    scaler_data = pickle.load(f)
    scaler = scaler_data['scaler']
    scaler_columns = scaler_data['columns']

# Initialize GA and inject scaler
ga = MealPlanGeneticAlgorithm(df)
ga.scaler = scaler  # for denormalization
ga.nutrition_cols = scaler_columns


def calculate_target_nutrition(user_data):
    """
    Calculate daily macro targets based on user calorie goal and selected goal type.
    """
    calories = user_data['adjustedCalories']
    goal = user_data['goal']

    ratios = {
        'Lose Weight': (0.35, 0.25, 0.40),
        'Build Muscle': (0.40, 0.20, 0.40),
        'Gain Weight': (0.25, 0.25, 0.50),
        'Maintain Weight': (0.30, 0.30, 0.40)
    }
    p_ratio, f_ratio, c_ratio = ratios.get(goal, (0.30, 0.30, 0.40))

    return {
        'calories': calories,
        'protein': (calories * p_ratio) / 4,   # grams (kcal/4)
        'fat': (calories * f_ratio) / 9,       # grams (kcal/9)
        'carbs': (calories * c_ratio) / 4      # grams (kcal/4)
    }


@app.route('/generate-meal-plan', methods=['POST'])
def generate_meal_plan():
    try:
        user_data = request.json

        days = user_data.get('days', DEFAULT_DAYS)

        # Build dietary restrictions dictionary
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

        target_nutrition = calculate_target_nutrition(user_data)

        # Run the genetic algorithm
        best_solution = ga.evolve(target_nutrition, dietary_restrictions, days)

        # best_solution is now a FLAT list of meal indices:
        # [breakfast_day1, lunch_day1, dinner_day1, breakfast_day2, ...]

        meal_plan = []
        meal_index = 0  # pointer into the flat list

        for day_idx in range(days):
            daily = {
                'day': day_idx + 1,
                'meals': [],
                'totalNutrition': {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0}
            }

            for meal_type in MEAL_TYPES:  # ['breakfast', 'lunch', 'dinner']
                if meal_index >= len(best_solution):
                    raise ValueError("Best solution length mismatch - not enough meals generated.")

                meal_idx = best_solution[meal_index]
                meal = df.iloc[meal_idx]

                # Denormalize nutrition values
                vals = meal[scaler_columns].values.reshape(1, -1)
                denorm = scaler.inverse_transform(vals)[0]
                nutrition_dict = dict(zip(scaler_columns, denorm))

                # Apply portion multiplier for realistic serving size
                multiplier = PORTION_MULTIPLIERS.get(meal_type, 1.0)
                scaled_nutrition = {k: v * multiplier for k, v in nutrition_dict.items()}

                cal = scaled_nutrition['calories']
                pro = scaled_nutrition['protein']
                fat = scaled_nutrition['fat']
                carb = scaled_nutrition['carbs']

                # Accumulate daily totals
                daily['totalNutrition']['calories'] += cal
                daily['totalNutrition']['protein'] += pro
                daily['totalNutrition']['fat'] += fat
                daily['totalNutrition']['carbs'] += carb

                # Build meal object for frontend
                meal_data = {
                    'meal_name': meal['meal_name'],
                    'calories': round(cal, 1),
                    'protein': round(pro, 1),
                    'fat': round(fat, 1),
                    'carbs': round(carb, 1),
                    'image_url': meal.get('image_url', ''),
                    'vitamins': meal.get('vitamins', ''),
                    'ingredients': meal['ingredients'].split(', ') if isinstance(meal.get('ingredients'), str) else [],
                    'sodium': round(scaled_nutrition.get('sodium_mg', 0), 1),
                    'sugar': round(scaled_nutrition.get('sugar_g', 0), 1),
                    'fiber': round(scaled_nutrition.get('fiber_g', 0), 1),
                    'cholesterol': round(scaled_nutrition.get('cholesterol_mg', 0), 1),
                    'portion_size_g': round(100 * multiplier, 0)
                }

                daily['meals'].append({meal_type: meal_data})
                meal_index += 1

            # Round daily totals
            for key in daily['totalNutrition']:
                daily['totalNutrition'][key] = round(daily['totalNutrition'][key], 1)

            meal_plan.append(daily)

        # Overall summary
        totals = [d['totalNutrition'] for d in meal_plan]
        nutrition_summary = {
            'avgCalories': round(sum(t['calories'] for t in totals) / days, 1),
            'avgProtein': round(sum(t['protein'] for t in totals) / days, 1),
            'avgFat': round(sum(t['fat'] for t in totals) / days, 1),
            'avgCarbs': round(sum(t['carbs'] for t in totals) / days, 1),
            'totalDays': days
        }

        return jsonify({
            'mealPlan': meal_plan,
            'nutritionSummary': nutrition_summary
        })

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to generate meal plan', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from models.meal_rl_agent import MealPlanRLAgent
from models.data_preprocessor import DataPreprocessor
import pickle
from config import SCALER_SAVE_PATH
import numpy as np

app = Flask(__name__)

# Initialize data preprocessor and load data
preprocessor = DataPreprocessor()
df = preprocessor.load_data()
df, _, _, _ = preprocessor.preprocess_data()

# Initialize RL agent
agent = MealPlanRLAgent(df)
if not agent.load_model():
    print("No saved model found. Please train the model first.")
    exit(1)

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

    # Calculate grams
    protein_g = (calories * protein_ratio) / 4
    fat_g = (calories * fat_ratio) / 9
    carbs_g = (calories * carb_ratio) / 4

    # Normalize for our scaled data
    target = {
        'calories': calories,
        'protein': protein_g,
        'fat': fat_g,
        'carbs': carbs_g
    }

    return target

@app.route('/generate-meal-plan', methods=['POST'])
def generate_meal_plan():
    user_data = request.json

    # Prepare dietary restrictions
    dietary_restrictions = {
        'vegetarian': user_data.get('dietType') == 'Vegetarian',
        'vegan': user_data.get('dietType') == 'Vegan',
        'keto': user_data.get('dietType') == 'Keto',
        'paleo': user_data.get('dietType') == 'Paleo',
        'gluten_free': user_data.get('dietType') == 'Gluten Free',
        'mediterranean': user_data.get('dietType') == 'Mediterranean',
        'allergies': user_data.get('allergies', [])
    }

    # Calculate targets
    target_nutrition = calculate_target_nutrition(user_data)
    days = user_data.get('days', 7)

    # Generate meal plan
    meal_plan = []
    current_nutrition = {
        'calories': 0,
        'protein': 0,
        'fat': 0,
        'carbs': 0
    }

    for day in range(days):
        daily_meals = {'day': day + 1, 'meals': [], 'totalNutrition': {}}

        for meal_type in ['breakfast', 'lunch', 'dinner']:
            state = agent.get_state_key(current_nutrition, days - day)
            action = agent.choose_action(state, dietary_restrictions)

            if action is None:
                daily_meals['meals'].append({
                    meal_type: {
                        'meal_name': 'No suitable meal found',
                        'calories': 0,
                        'protein': 0,
                        'fat': 0,
                        'carbs': 0,
                        'image_url': '',
                        'vitamins': ''
                    }
                })
                continue

            selected_meal = df.iloc[action]

            # Update nutrition
            current_nutrition['calories'] += selected_meal['calories'] * scaler.data_max_[0]
            current_nutrition['protein'] += selected_meal['protein'] * scaler.data_max_[1]
            current_nutrition['fat'] += selected_meal['fat'] * scaler.data_max_[2]
            current_nutrition['carbs'] += selected_meal['carbs'] * scaler.data_max_[3]

            # Calculate reward and update Q-table
            next_state = agent.get_state_key({
                'calories': current_nutrition['calories'] / scaler.data_max_[0],
                'protein': current_nutrition['protein'] / scaler.data_max_[1],
                'fat': current_nutrition['fat'] / scaler.data_max_[2],
                'carbs': current_nutrition['carbs'] / scaler.data_max_[3]
            }, days - day - 1)

            reward = agent.calculate_reward(action, {
                'calories': current_nutrition['calories'] / scaler.data_max_[0],
                'protein': current_nutrition['protein'] / scaler.data_max_[1],
                'fat': current_nutrition['fat'] / scaler.data_max_[2],
                'carbs': current_nutrition['carbs'] / scaler.data_max_[3]
            }, {
                                                'calories': target_nutrition['calories'] / scaler.data_max_[0],
                                                'protein': target_nutrition['protein'] / scaler.data_max_[1],
                                                'fat': target_nutrition['fat'] / scaler.data_max_[2],
                                                'carbs': target_nutrition['carbs'] / scaler.data_max_[3]
                                            }, day)

            agent.update_q_table(state, action, reward, next_state)

            # Add meal to plan
            meal_data = {
                'meal_name': selected_meal['meal_name'],
                'calories': float(selected_meal['calories'] * scaler.data_max_[0]),
                'protein': float(selected_meal['protein'] * scaler.data_max_[1]),
                'fat': float(selected_meal['fat'] * scaler.data_max_[2]),
                'carbs': float(selected_meal['carbs'] * scaler.data_max_[3]),
                'image_url': selected_meal['image_url'],
                'vitamins': selected_meal['vitamins']
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

if __name__ == '__main__':
    app.run(debug=True)

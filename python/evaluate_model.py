from models.meal_rl_agent import MealPlanRLAgent
from models.data_preprocessor import DataPreprocessor
import numpy as np
from config import COMMON_ALLERGENS

def calculate_model_accuracy(agent, test_cases=10):
    total_score = 0
    successful_cases = 0

    for _ in range(test_cases):
        # Create random test case
        diet_type = np.random.choice(['vegetarian', 'vegan', 'keto', 'paleo', 'gluten_free', 'mediterranean', 'none'])
        allergies = np.random.choice(list(COMMON_ALLERGENS.keys()), np.random.randint(0, 3), replace=False)

        dietary_restrictions = {
            'vegetarian': diet_type == 'vegetarian',
            'vegan': diet_type == 'vegan',
            'keto': diet_type == 'keto',
            'paleo': diet_type == 'paleo',
            'gluten_free': diet_type == 'gluten_free',
            'mediterranean': diet_type == 'mediterranean',
            'allergies': list(allergies)
        }

        calories = np.random.randint(1500, 3000)
        target = {
            'calories': calories,
            'protein': calories * 0.3 / 4,
            'fat': calories * 0.3 / 9,
            'carbs': calories * 0.4 / 4
        }

        # Test one day (3 meals)
        daily_score = 0
        valid_meals = 0

        for _ in range(3):  # breakfast, lunch, dinner
            action = agent.choose_action(
                agent.get_state_key(
                    {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0},
                    1  # days remaining
                ),
                dietary_restrictions
            )

            if action is not None:
                meal = agent.meals.iloc[action]
                # Calculate how close meal is to 1/3 of daily target
                calorie_diff = abs(target['calories']/3 - meal['calories']*100)
                protein_diff = abs(target['protein']/3 - meal['protein']*100)

                # Simple score (0-100)
                meal_score = 100 - (calorie_diff/50 + protein_diff/10)
                daily_score += max(0, min(100, meal_score))
                valid_meals += 1

        if valid_meals > 0:
            total_score += daily_score / valid_meals
            successful_cases += 1

    if successful_cases > 0:
        accuracy = total_score / successful_cases
        print(f"Model Accuracy: {accuracy:.1f}%")
    else:
        print("Could not calculate accuracy - no valid test cases")

if __name__ == '__main__':
    preprocessor = DataPreprocessor()
    df = preprocessor.load_data()
    df, _, _, _ = preprocessor.preprocess_data()

    agent = MealPlanRLAgent(df)
    if agent.load_model():
        calculate_model_accuracy(agent)
    else:
        print("Error: No trained model found")

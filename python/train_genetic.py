# train_genetic.py

from models.genetic_algorithm import MealPlanGeneticAlgorithm
from models.data_preprocessor import DataPreprocessor
import random
import pickle
from config import COMMON_ALLERGENS, DIET_TYPE_MAPPING, DEFAULT_NUTRITION_TARGETS, SCALER_SAVE_PATH

def train_genetic_algorithm(ga, num_training_cases=50):
    print(f"Training Genetic Algorithm with {num_training_cases} training cases...")
    for case in range(num_training_cases):
        if (case + 1) % 10 == 0:
            print(f"Training case {case + 1}/{num_training_cases}")

        goal = random.choice(['Lose Weight', 'Build Muscle', 'Gain Weight', 'Maintain Weight'])
        diet_type = random.choice(list(DIET_TYPE_MAPPING.keys()))
        allergies = random.sample(list(COMMON_ALLERGENS.keys()), random.randint(0, 2))
        health_risks = random.sample([
            'High blood pressure', 'High cholesterol', 'Diabetes',
            'Heart disease or stroke', 'Testosterone deficiency', 'Depression'
        ], random.randint(0, 2))

        dietary_restrictions = {
            'vegetarian': diet_type == 'Vegetarian',
            'vegan': diet_type == 'Vegan',
            'keto': diet_type == 'Keto',
            'paleo': diet_type == 'Paleo',
            'gluten_free': diet_type == 'Gluten Free',
            'mediterranean': diet_type == 'Mediterranean',
            'allergies': allergies,
            'health_risks': health_risks
        }

        calories = random.randint(1500, 3000)
        ratios = DEFAULT_NUTRITION_TARGETS[goal]
        target_nutrition = {
            'calories': calories,
            'protein': (calories * ratios['protein_ratio']) / 4,
            'fat': (calories * ratios['fat_ratio']) / 9,
            'carbs': (calories * ratios['carb_ratio']) / 4
        }

        days = random.randint(3, 7)
        ga.evolve(target_nutrition, dietary_restrictions, days)

    try:
        ga.save_model()
        print("Training completed. Model saved.")
    except Exception as e:
        print(f"Error saving model: {e}")

if __name__ == '__main__':
    preprocessor = DataPreprocessor()
    df = preprocessor.load_data()
    df, scaler, vitamins, diet_cols = preprocessor.preprocess_data()

    ga = MealPlanGeneticAlgorithm(df)
    ga.scaler = scaler  # inject for accurate calculations
    ga.nutrition_cols = preprocessor.scaler.feature_names_in_ if hasattr(scaler, 'feature_names_in_') else None  # or use NUTRITION_COLS

    train_genetic_algorithm(ga, num_training_cases=100)

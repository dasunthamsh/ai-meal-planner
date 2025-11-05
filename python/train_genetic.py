from models.genetic_algorithm import MealPlanGeneticAlgorithm
from models.data_preprocessor import DataPreprocessor
import random
from config import COMMON_ALLERGENS, DIET_TYPE_MAPPING, DEFAULT_NUTRITION_TARGETS

def train_genetic_algorithm(ga, num_training_cases=50):
    print(f"Training Genetic Algorithm with {num_training_cases} training cases...")

    for case in range(num_training_cases):
        if (case + 1) % 10 == 0:
            print(f"Training case {case + 1}/{num_training_cases}")

        # Get random user preferences for training
        goal = random.choice(['Lose Weight', 'Build Muscle', 'Gain Weight', 'Maintain Weight'])
        diet_type = random.choice(list(DIET_TYPE_MAPPING.values()))
        allergies = random.sample(list(COMMON_ALLERGENS.keys()), random.randint(0, 2))
        health_risks = random.sample([
            'High blood pressure', 'High cholesterol', 'Diabetes',
            'Heart disease or stroke', 'Testosterone deficiency', 'Depression'
        ], random.randint(0, 2))

        dietary_restrictions = {
            'vegetarian': diet_type == 'vegetarian',
            'vegan': diet_type == 'vegan',
            'keto': diet_type == 'keto',
            'paleo': diet_type == 'paleo',
            'gluten_free': diet_type == 'gluten_free',
            'mediterranean': diet_type == 'mediterranean',
            'allergies': allergies,
            'health_risks': health_risks
        }

        # Calculate target nutrition based on goal
        calories = random.randint(1500, 3000)
        nutrition_targets = DEFAULT_NUTRITION_TARGETS[goal]

        protein_g = (calories * nutrition_targets['protein_ratio']) / 4
        fat_g = (calories * nutrition_targets['fat_ratio']) / 9
        carbs_g = (calories * nutrition_targets['carb_ratio']) / 4

        target_nutrition = {
            'calories': calories,
            'protein': protein_g,
            'fat': fat_g,
            'carbs': carbs_g
        }

        # Run evolution for this training case
        days = random.randint(3, 7)
        ga.evolve(target_nutrition, dietary_restrictions, days)

    try:
        ga.save_model()
        print("Training completed. Model saved.")
    except Exception as e:
        print(f"Error saving model: {e}")
        print("Training completed but model could not be saved.")

if __name__ == '__main__':
    preprocessor = DataPreprocessor()
    df = preprocessor.load_data()
    df, scaler, vitamins, diet_cols = preprocessor.preprocess_data()

    ga = MealPlanGeneticAlgorithm(df)

    train_genetic_algorithm(ga, num_training_cases=100)

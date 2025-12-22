import random
import numpy as np
from models.genetic_algorithm import MealPlanGeneticAlgorithm
from models.data_preprocessor import DataPreprocessor
from config import DEFAULT_NUTRITION_TARGETS, DIET_TYPE_MAPPING, COMMON_ALLERGENS

def calculate_algorithm_accuracy(num_test_cases=50):

    print(f"Testing Genetic Algorithm Accuracy with {num_test_cases} test cases...")

    # Initialize data preprocessor and load data
    preprocessor = DataPreprocessor()
    df = preprocessor.load_data()
    df, _, _, _ = preprocessor.preprocess_data()

    # Initialize Genetic Algorithm
    ga = MealPlanGeneticAlgorithm(df)

    fitness_scores = []
    successful_cases = 0
    total_calorie_error = 0
    total_protein_error = 0

    for case in range(num_test_cases):
        try:
            # Generate random user profile for testing
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

            # Calculate target nutrition
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

            days = random.randint(3, 7)

            # Generate meal plan
            best_solution = ga.evolve(target_nutrition, dietary_restrictions, days)

            # Calculate fitness score for this solution
            fitness = ga.calculate_fitness(best_solution, target_nutrition, dietary_restrictions)
            fitness_scores.append(fitness)

            # Count as successful if fitness is above threshold
            if fitness > 0.6:  # Adjust threshold as needed
                successful_cases += 1

            # Calculate nutrition accuracy
            actual_calories, actual_protein = calculate_actual_nutrition(best_solution, df, days)
            target_total_calories = target_nutrition['calories'] * days
            target_total_protein = target_nutrition['protein'] * days

            calorie_error = abs(actual_calories - target_total_calories) / target_total_calories
            protein_error = abs(actual_protein - target_total_protein) / target_total_protein

            total_calorie_error += calorie_error
            total_protein_error += protein_error

            if (case + 1) % 10 == 0:
                print(f"Completed {case + 1}/{num_test_cases} test cases...")

        except Exception as e:
            print(f"Error in test case {case + 1}: {e}")
            continue

    # Calculate accuracy metrics
    if fitness_scores:
        average_fitness = np.mean(fitness_scores)
        success_rate = (successful_cases / num_test_cases) * 100
        avg_calorie_accuracy = (1 - (total_calorie_error / num_test_cases)) * 100
        avg_protein_accuracy = (1 - (total_protein_error / num_test_cases)) * 100
        overall_accuracy = (average_fitness * 100)  # Convert fitness to percentage

        print("\n" + "="*50)
        print("ALGORITHM ACCURACY RESULTS")
        print("="*50)
        print(f"Average Fitness Score: {average_fitness:.4f}")
        print(f"Overall Accuracy: {overall_accuracy:.2f}%")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Calorie Accuracy: {avg_calorie_accuracy:.2f}%")
        print(f"Protein Accuracy: {avg_protein_accuracy:.2f}%")
        print(f"Test Cases: {num_test_cases}")
        print(f"Successful Cases: {successful_cases}")

        # Accuracy rating
        if overall_accuracy >= 80:
            rating = "EXCELLENT"
        elif overall_accuracy >= 70:
            rating = "GOOD"
        elif overall_accuracy >= 60:
            rating = "FAIR"
        else:
            rating = "NEEDS IMPROVEMENT"

        print(f"Accuracy Rating: {rating}")

        return {
            'overall_accuracy': overall_accuracy,
            'average_fitness': average_fitness,
            'success_rate': success_rate,
            'calorie_accuracy': avg_calorie_accuracy,
            'protein_accuracy': avg_protein_accuracy,
            'total_test_cases': num_test_cases,
            'successful_cases': successful_cases,
            'rating': rating
        }
    else:
        print("No valid test cases completed.")
        return None

def calculate_actual_nutrition(meal_plan, df, days):
    """Calculate actual nutrition from generated meal plan"""
    total_calories = 0
    total_protein = 0
    serving_size = 100

    for day_meals in meal_plan:
        for meal_type, meal_idx in day_meals.items():
            meal = df.iloc[meal_idx]
            total_calories += meal['calories'] * serving_size
            total_protein += meal['protein'] * serving_size

    return total_calories, total_protein

def validate_single_case():
    """Test a single specific case for detailed analysis"""
    preprocessor = DataPreprocessor()
    df = preprocessor.load_data()
    df, _, _, _ = preprocessor.preprocess_data()

    ga = MealPlanGeneticAlgorithm(df)

    # Test a specific case
    target_nutrition = {
        'calories': 2000,
        'protein': 150,  # 2000 * 0.3 / 4
        'fat': 67,       # 2000 * 0.3 / 9
        'carbs': 200     # 2000 * 0.4 / 4
    }

    dietary_restrictions = {
        'vegetarian': False,
        'vegan': False,
        'keto': False,
        'paleo': False,
        'gluten_free': False,
        'mediterranean': False,
        'allergies': [],
        'health_risks': []
    }

    days = 7

    print("Testing single case...")
    best_solution = ga.evolve(target_nutrition, dietary_restrictions, days)
    fitness = ga.calculate_fitness(best_solution, target_nutrition, dietary_restrictions)

    print(f"Single Case Fitness: {fitness:.4f}")
    print(f"Single Case Accuracy: {fitness * 100:.2f}%")

    return fitness * 100

if __name__ == '__main__':
    # Run comprehensive accuracy test
    results = calculate_algorithm_accuracy(num_test_cases=50)

    print("\n" + "="*50)
    print("ADDITIONAL VALIDATION")
    print("="*50)

    # Test single case for quick validation
    single_accuracy = validate_single_case()
    print(f"Quick Validation Accuracy: {single_accuracy:.2f}%")
